# hubblax
Simple snia standardisation tools based on jax.

= this package is temporary and is likely to be replaced by edris ; stay tuned =

# Sharp start

## Step 1. simulate data
```python
import skysurvey
# Model (truth)
ntargets = 1_000
magabs_model = {"beta":3.15, "alpha":-0.14, "sigmaint":0.1, "mabs":-19}

# Perfect targets
snia = skysurvey.SNeIa.from_draw(ntargets, magabs=magabs_model)
## store the Hubble residuals
snia.data["mag"] = snia.data["magobs"] - snia.magabs_to_magobs(snia.data["z"], magabs=magabs_model["mabs"])

# Apply covariant noise
from skysurvey.tools import utils
noisemodel = { "x1": 0.11, "c":0.09, "mag": 0.01, 
              "cov_cx1": 0, "cov_x1mag":0, "cov_cmag":0}
snianoisy = utils.apply_gaussian_noise(snia, **noisemodel)
data = snianoisy.data.copy()
```

## Step 2. load Hubblax
```python
import jax.numpy as jnp
# truth is optional
truth = {"coefs": (magabs_model["alpha"], magabs_model["beta"]),
         "offset":0,
         "sigma":magabs_model["sigmaint"],
         "variables": jnp.asarray(snia.data[["x1", "c"]].values.T, dtype="float32")
         }
h = hubblax.Hubblax.from_data(data, truth=truth, incl_cov=True)
```

## Step 3. fit
```python
# guess is optional
guess_coefs = np.asarray(h.truth["coefs"])+(0.1,-0.1)
guess = h.get_guess(guess_coefs)#, sigma=0.1)
param, loss = h.fit(guess=guess, niter=150, force_sigma=truth["sigma"])
```

## Step 4. see the results
```python
fig = h.show(params=param, loss=loss)
```
![](gallery/example_plot.png)
