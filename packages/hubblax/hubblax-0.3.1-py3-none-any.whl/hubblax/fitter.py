import optax
import jax

def fit_adam(func, init_params,
                 learning_rate=5e-3, niter=200, 
                 retloss=False,
                 **kwargs):
    """ """
    # such that only gradient only on params
    
    params = init_params
    optimizer = optax.adam(learning_rate)
    
    # Obtain the `opt_state` that contains statistics for the optimizer.
    opt_state = optimizer.init(params)
    grad_func = jax.jit(jax.grad( func ))
    
    loss = []
    for _ in range(niter):
        current_grads = grad_func(params)
        updates, opt_state = optimizer.update(current_grads, opt_state)
        params = optax.apply_updates(params, updates)
        if retloss:
            loss.append( func(params) )
        
    if retloss:
        return params, loss
    
    return params
