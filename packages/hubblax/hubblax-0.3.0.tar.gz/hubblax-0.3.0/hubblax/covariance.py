import warnings

import jax
import jax.numpy as jnp
import tree_math as tm

import numpy as np


""" This is adapted from edris: 
https://gitlab.in2p3.fr/groupe-edris

Math credit: Marc Betoule
"""


def compute_fastcov_chi2(q, lambda_, inv_cxx, cov_yx, delta_y, delta_x, sigmaint):
    """ fast chi2 and logdet computation from reshaped covariance matrix elements.
    
    Parameters
    ----------

    delta_y: jnp.array 
        residual between observed_y - model_y (N,)

    delta_x: jnp.array 
        residual between observed_x - model_x (M, N)

    sigmaint: jnp.array
        intrinsic dispersion () or (N,)


    Returns
    -------
    chi2, logdet
    """
    qr = q.T @ delta_y
    inv_sdiag = 1/(lambda_ + sigmaint**2)
    inv_c2r = inv_cxx @ delta_x
    c1_inv_c2r = cov_yx @ inv_c2r
    s_c1_inv_c2r = (delta_y.T * c1_inv_c2r) * inv_sdiag
    rwr = ((qr ** 2 * inv_sdiag).sum()
            -2 * s_c1_inv_c2r.sum()
            + (delta_x * inv_c2r).sum()
            + (c1_inv_c2r **2 * inv_sdiag).sum()
           )
    
    return rwr, -jnp.log(inv_sdiag).sum()


def fill_diagonal(a, val):
    """ fast diagonal filler """
    assert a.ndim >= 2
    i, j = jnp.diag_indices(min(a.shape[-2:]))
    return a.at[..., i, j].set(val)


class CovChi2( object ):
    
    def __init__(self, cov_yy=None, cov_xx=None, cov_yx=None, initialize=True):
        self._cov_yy = cov_yy # (N, N)
        self._cov_xx = cov_xx # (M*N, M*N)
        self._cov_yx = cov_yx # (N, M*N)
        if initialize:
            self._initialize()

    def copy(self):
        """ """
        from copy import deepcopy
        return deepcopy(self) # copies the __dict__

    @classmethod
    def from_data(cls, data, ykey="mag", xkeys=["x1","c"], 
                   suffix_err="_err", prefix_cov="cov_",
                      **kwargs):
        """ creates the cov_yy, cov_xy and cov_xx matrices out of a dataframe

        Parameters
        ----------
        data: pandas.DataFrame
            pandas dataframe containing the data

        ykey: string
            name of the y-columns

        xkeys: list
            list of column containing the x-parameters

        suffix_err: string
            format for the error columns such that "{xkey}{suffix_err}"

        prefix_cov: string
            format for the covariance columns such that 
            "cov_{xkey1}{xkey2}"

        **kwargs goes to class' __init__

        Returns
        -------
        list
            list of three jax array
            - cov_yy: (N,N)
            - cov_xy: (N, N*M)
            - cov_xx: (N*M, N*M)


        Format:
        -------

        ------------
        | yy | yx  |
        -----------|
             | xx  |
             |-----|


        """
        # this method is sparse based, so ready for sparse analyses.
        
        from jax.experimental import sparse

        data_ = data.copy() # work on the copy

        ntargets = len(data)
        mcoefs = len(xkeys)

        # make sure they are errors on x
        xerrkeys = [f"{k}_err" for k in xkeys]
        for k in xerrkeys:
            if k not in data_.columns:
                data_[k] = 0
        data_[xerrkeys] = data_[xerrkeys]**2 # variance
        
        #
        # cov_yy
        #
        y_err = data_.get(f"{ykey}{suffix_err}", np.zeros(ntargets))**2
        cov_yy = jnp.diag(jnp.asarray(y_err))

        #
        # cov_xy/cov_yx
        #
        keyscov_keys = [[i, covkey] 
                for i,xi in enumerate(xkeys)
                if (covkey := f"{prefix_cov}{xi}{ykey}") in data_.columns or
                   (covkey := f"{prefix_cov}{ykey}{xi}") in data_.columns] 
                # never goes to second line if first accepted


        col_index = np.asarray([l[0] for l in keyscov_keys])
        cov_keys = [l[1] for l in keyscov_keys]


        row = np.arange(ntargets) * np.ones(mcoefs)[:,None]
        col = np.arange(ntargets)[:,None]*mcoefs + np.arange(mcoefs)
        covdata = np.zeros_like(col, dtype="float")
        covdata[:,col_index] = data[cov_keys].values
        coo_yx = sparse.COO((covdata.flatten(), 
                             row.T.flatten().astype(int), 
                             col.flatten()), 
                             shape=(ntargets,ntargets*mcoefs))
        cov_yx = coo_yx.todense()

        #
        # cov_xx
        #

        # make sure the x_err are in        
        keyscov_keys = [[(i,j),covkey] 
                        for i,xi in enumerate(xkeys)
                        for j,xj in enumerate(xkeys) 
                        if (covkey := f"{prefix_cov}{xj}{xi}") in data_.columns]

        col_, row_ = np.asarray([l[0] for l in keyscov_keys]).T
        cov_keys = [l[1] for l in keyscov_keys]
        xerrkeys += cov_keys


        xdata = data_[xerrkeys].values
        # using sparse matrix tools
        xrow = np.append(np.arange(mcoefs),list(row_)) + np.arange(ntargets)[:,None]*mcoefs
        xcol = np.append(np.arange(mcoefs),list(col_)) + np.arange(ntargets)[:,None]*mcoefs
        coo_xx = sparse.COO( (xdata.flatten(), 
                           xrow.flatten(), 
                           xcol.flatten()), 
                           shape=(ntargets*mcoefs, ntargets*mcoefs) )

        # make it full and square per block
        dense_xx = coo_xx.todense()
        cov_xx = dense_xx + fill_diagonal(dense_xx, 0).T

        return cls(cov_yy=cov_yy, cov_yx=cov_yx, cov_xx=cov_xx, **kwargs)

    def _initialize(self):
        """ Precompute a few matrices to speed up __call__ """
        if "Metal" not in str(jax.devices()): # not ready
            self._inv_cxx = jnp.linalg.inv(self.cov_xx)
            jax_ok = True
            _jnp = jnp
                
        else: # numpy back-up
            self._inv_cxx = np.linalg.inv( self.cov_xx.astype("float32") )
            jax_ok = False
            _jnp = np

        self._inv_cxx_cyx = self._inv_cxx @ self.cov_yx.T
        self._lambda, self._q = _jnp.linalg.eig(self.cov_yy - _jnp.dot(self.cov_yx, self._inv_cxx_cyx))

        if not jax_ok: # jax.array what is needed.
            self._inv_cxx = jnp.asarray(self._inv_cxx, dtype="float32")
            self._lambda = jnp.asarray(self._lambda, dtype="float32")
            self._q = jnp.asarray(self._q, dtype="float32")
        else: # make sure it is float
            self._lambda = self._lambda.astype(float)
            self._q = self._q.astype(float)

    def __call__(self, delta_y, delta_x, sigmaint=0, **kwargs):
        """ calls compute_chi2logdet"""
        chi2, logdet = self.compute_chi2logdet(delta_y, delta_x, sigmaint=0, **kwargs)
        return chi2, logdet

    # ================ #
    #  Generic method  #
    # ================ #
    def get(self, value, default=None):
        """ access instance variables. 
        This method follows the pytree/dict format 
        """
        return getattr(self, value, getattr(self, f"_{value}", default))

    def compute_chi2logdet(self, delta_y, delta_x, sigmaint=0):
        """ Compute the chi2 for a given residual vector and the variable part of the logdet

        chi^2 evaluation is only O(N^2)

        Parameters
        ----------
        delta_y: jnp.array 
            residual between observed_y - model_y (N,)

        delta_x: jnp.array 
            residual between observed_x - model_x (M, N)

        sigmaint: float, jnp.array
            intrinsic dispersion () or (N,)

        Returns
        -------
        chi2, logdet
        """
        # F as x1_vec, x2_vec because (x1_0, x2_0, x1_1, x1_1 etc.)
        flat_delta_x = delta_x.ravel("F")
        
        chi2, logdet = compute_fastcov_chi2(q=self._q, lambda_=self._lambda,
                                                inv_cxx=self._inv_cxx, 
                                                cov_yx=self.cov_yx,
                                                delta_y=delta_y, #(N,)
                                                delta_x=flat_delta_x, #(N*M,)
                                                sigmaint=sigmaint)
        return chi2, logdet
    
    # ================ #
    #    Properties    #
    # ================ #
    @property
    def cov_yy(self):
        """ covariance between y parameters 
        shape: (N, N) 
        """
        return self._cov_yy
    
    @property    
    def cov_xx(self):
        """ covariance between variable parameters 
        shape: (N*M, N*M) 
        """
        return self._cov_xx
    
    @property
    def cov_yx(self):
        """ covariance between y and variable parameters 
        shape: (N, N*M) 
        """
        return self._cov_yx

    @property
    def x_err(self):
        """ sqrt of cov_xx diag"""
        return jnp.sqrt( jnp.diag(self.cov_xx) )
   
    @property
    def y_err(self):
        """ sqrt of cov_yy diag"""
        return jnp.sqrt( jnp.diag(self.cov_yy) )

    
