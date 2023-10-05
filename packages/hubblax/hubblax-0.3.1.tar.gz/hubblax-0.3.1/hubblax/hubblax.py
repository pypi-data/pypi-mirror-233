import jax
import numpy as np
import jax.numpy as jnp
from . import likelihood as hlike
from . import fitter as hfitter


class Hubblax():
    """ """
    def __init__(self, observations, errors, truth=None):
        """ """
        self._observations = observations
        self._errors = errors
        self._truth = truth
        
    @classmethod
    def from_data(cls, data, 
                      y_key="mag", x_keys=["x1","c"],
                      truth=None,
                      incl_cov=True,
                      precision="float32"):
        """ """
        x_keys = np.atleast_1d(x_keys) 

        # observations
        y_obs = jnp.asarray(data[f"{y_key}"].values, dtype=precision)
        x_obs = jnp.asarray(data[x_keys].values.T, dtype=precision)
        observations = (y_obs, x_obs)

        # errors
        if not incl_cov:
            y_err = jnp.asarray(data[f"{y_key}_err"].values, dtype=precision)
            x_err = jnp.asarray(data[[f"{l}_err" for l in x_keys]].values.T, dtype=precision)
            errors = {"y_err": y_err, "x_err": x_err}
        else:
            from .covariance import CovChi2
            errors = CovChi2.from_data(data, initialize=True)
            
        return cls(observations, errors, truth=truth)
    
    # ============ #
    #  Method      #
    # ============ #
    def get_guess(self, coefs=None, offset=0, sigma=1):
        """ """
        if coefs is None:
            coefs = jnp.ones((self.ncoefs,))
            
        return {"coefs": jnp.asarray(coefs, dtype="float32"), # standardisation coef
                "offset": jnp.asarray(offset, dtype="float32"), 
                "sigma": jnp.asarray(sigma, dtype="float32"), # intrinsic
                "variables": self.x_obs  # standardization param
               }

    def fit(self, guess=None, force_sigma=None,
                likelihood="loglikelihood",
                fitter="adam", **kwargs):
        """ """
        if guess is None:
            guess = self.get_guess()

        
        if force_sigma:
            errors = self.errors.copy()
            _ = guess.pop("sigma") # not fitted anymore
            if "CovChi2" in str( type(errors) ):
                errors.sigma = jnp.asarray(force_sigma)
            else:
                errors["sigma"] = jnp.asarray(force_sigma)
        else:
            errors = self.errors
            
        # function to fit
        if type(likelihood) is str:
            likelihood_func = eval(f"hlike.{likelihood}")
        else: # assume function
            likelihood_func = likelihood

            
        # could include sigma
        fit_func = lambda x: likelihood_func(x, self.observations, errors)
        fit_func = jax.jit(fit_func)

        # fitter method
        if type(fitter) is str:
            fit_function = eval(f"hfitter.fit_{fitter}")
        else: # assumed function
            fit_function = fitter
            
        params, loss = fit_function(func=fit_func,
                                init_params=guess,
                                retloss=True,
                                **kwargs)
        return params, loss
    
    def show(self, params=None, loss=None, 
             fig=None, axes=None, axloss=None,
             paramprop={},
             **kwargs):
        """ 
        """
        import matplotlib.pyplot as plt
        from matplotlib.gridspec import GridSpec

        y_obs, x_obs = self.observations
        y_err, x_err = self.errors.get("y_err", 0), self.errors.get("x_err",0)
        truth = self.truth

        # - figures & axes    
        if axes is None:
            if fig is None:
                fig = plt.figure(figsize=[3+3*self.ncoefs,3])
            # coefficients
            left = 0.3 if loss is not None else 0.05
            gs = GridSpec(1, self.ncoefs, left=left, bottom=0.2, right=0.98, wspace=0.05)
            axes = [fig.add_subplot(gs[i]) for i in range(self.ncoefs)]
        else:
            fig = axes[0].figure 

        # - properties
        prop = {**dict(ls='none', color='k', alpha=0.2, marker='.', zorder=3),
                **kwargs}
        # - 
        for i in range(self.ncoefs):
            ax = axes[i]
            ax.errorbar(x_obs[i], y_obs, 
                        yerr=y_err, 
                        xerr=x_err[i],
                       **prop)

            if truth is not None:
                x = (x_obs[i].min(), x_obs[i].max())
                y = np.polyval([truth['coefs'][i], truth['offset']], x)
                ax.plot(x, y, ls="-", color="tab:red", zorder=4)

            if params is not None:
                x = (x_obs[i].min(), x_obs[i].max())
                y = np.polyval([params['coefs'][i], params['offset']], x)
                ax.plot(x, y, **{**{"zorder":4, "ls":"--", "lw":2},**paramprop})

            # labels
            ax.set_xlabel(f"x_{i}")
            if i>0:
                ax.set_yticklabels([])
            else:
                ax.set_ylabel("y")

        if loss:
            if axloss is None:
                gsloss = GridSpec(1, 1, left=0.05, right=0.2, bottom=0.2)
                axloss = fig.add_subplot(gsloss[0])

            axloss.plot(loss)
            clearwhich = ["right","top", "left"] # "bottom"
            [axloss.spines[which].set_visible(False) for which in clearwhich]
            axloss.set_yticks([])
            axloss.set_xlabel("iterations")

        return fig
        
    # ============ #  
    #  Properties  #
    # ============ #
    @property
    def observations(self):
        return self._observations
    
    @property
    def errors(self):
        return self._errors

    @property
    def y_obs(self):
        """ y-observations (N,) """
        return self._observations[0]

    @property
    def x_obs(self):
        """ x-observations (M, N) """
        return self._observations[1]
    
    @property
    def nvalues(self):
        return len(self.y_obs) # (N,)

    @property
    def ncoefs(self):
        return len(self.x_obs) # (M, N)
    
    @property
    def truth(self):
        return self._truth
