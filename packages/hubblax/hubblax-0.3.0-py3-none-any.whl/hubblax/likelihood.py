import jax
import jax.numpy as jnp

import optax

import jax
import jax.numpy as jnp

import optax

def params_to_model(params):
    """ convert the parameters into model y and model x

    Parameters:
    -----------
    params: pytreee
        a jax pytree providing 
        - coefs (N,)
        - variables (M, N)
        - offset ()
    
    Returns
    -------
    list
        - model_y (N,) 
        - model_x (M, N)
    """
    model_y = jnp.dot(params['coefs'], params["variables"]) + params['offset']
    model_x = params["variables"]
    return model_y, model_x

def loglikelihood(params, observations, errors):
    """ Full likelihood for the "y_j = a^i x_ij + offset" model
    
    There are N values (len(y)) for M variables
    
    Parameters
    ----------
    params: pytree
        a jax pytree providing:
        - coefs  (M,)
        - offset ()
        - variables (M, N)
        [ - sigma () ] optional

    observed: list
        observed data with the format (y, x):
        - y (N,)
        - x (M, N)
        
    errors: pytree
        pytree containing the observation errors
        - y_err (N,)
        - x_err (M, N)
        [ - sigma () ] optional, ignored if given in params

    Returns
    -------
    float
    """
    # Observations
    chi2, logdet = get_chi2(params, observations, errors)

    # likelihood
    loglikelihood = chi2 + logdet
    return loglikelihood

# =============== #
#                 #
#    Tools        #
#                 #
# =============== #
def fetch_sigma(params, errors, default=0., key="sigma"):
    """ fetch sigmaint from params (first) and errors (next).
    If none found, default is returned
    """

    # errors could either be a pytree or a CovChi2
    sigmaint = params.get(key, errors.get(key, default))
    return sigmaint

def get_chi2(params, observations, errors):
    """ Full likelihood for the "y_j = a^i x_ij + offset" model
    
    There are N values (len(y)) for M variables
    
    Parameters
    ----------
    params: pytree
        a jax pytree providing:
        - coefs (M,)
        - offset ()
        - variables (M, N)
        [ - sigma () ] optional

    observed: list
        observed data with the format (y, x):
        - y (N,)
        - x (M, N)
        
    errors: pytree, CovChi2
        two format are available, depending if there is covariance or not:
        - no covariance, simply provide the errors as a pytree
           - y_err (N,)
           - x_err (M, N)
           [ - sigma () ] optional, ignored if given in params

        - covariance, provide the hubblax.CovChi2 object
        

    Returns
    -------
    float, float
        - chi2: jnp.sum(chi2_y) + jnp.sum(chi2_x)
        - logdet: jnp.sum( jnp.log(sigmaint**2 + y_err**2) )
    """
    # comment information: N=number of targets, M=number variables

    # Observations
    observed_y, observed_x = observations      # (N,), (M, N)
    model_y, model_x = params_to_model(params) # (N,), (M, N)

    delta_y = observed_y - model_y
    delta_x = observed_x - model_x

    # try params["sigma"] first, errors["sigma"] second, and sets 0 otherwise
    sigmaint = fetch_sigma(params, errors)
    if "CovChi2" in str(type(errors)):
        chi2, logdet = errors(delta_y, delta_x, sigmaint=sigmaint)
    else:
        sigma2 = sigmaint**2 + errors["y_err"]**2     # (N,)
        chi2_y = (delta_y)**2 / sigma2                # (N,)
        chi2_x = (delta_x)** 2 / errors["x_err"]**2   # (M, N)
    
        # log likelihood | the last term should be ntargets_*jnp.log(sigma2) if sigma2 is a float
        chi2 = jnp.sum(chi2_y) + jnp.sum(chi2_x)
        logdet = jnp.sum( jnp.log(sigma2) ) # float
        
    return chi2, logdet
