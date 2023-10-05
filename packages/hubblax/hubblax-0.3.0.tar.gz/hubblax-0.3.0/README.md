# hubblax
Simple snia standardisation tools based on jax.

= this package is temporary and is likely to be replaced by edris ; stay tuned =

# Sharp start

## Step 1. simulate data
```python
import skysurvey
from skysurvey.tools import apply_gaussian_noise

ntargets = 1_000
magabs_model = {"beta":3.3, "alpha":0.2, "sigmaint":0.08, "mabs":-19}
error_model = {"x1":0.4, "c":0.1, "magobs":0.1}

snia = skysurvey.SNeIa.from_draw(ntargets, magabs=magabs_model)
snianoisy = apply_gaussian_noise(snia, **error_model)
data = snianoisy.data

# creating the Hubble residual to avoid fitting cosmology
data["mag"] = data["magobs"] - snianoisy.magabs_to_magobs(data["z"], magabs=magabs_model["mabs"])
data["mag_err"] = data["magobs_err"]
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
h = hubblax.Hubblax.from_data(data, truth=truth)
```

## Step 3. fit
```python
# guess is optional
guess_coefs = np.asarray(h.truth["coefs"])+(0.2,-0.1)
guess = h.get_guess(coefs=guess_coefs, sigma=0.1)
param, loss = h.fit(guess=guess, niter=300)
```

## Step 4. see the results
```python
fig = h.show(params=param, loss=loss)
```
![](gallery/example_plot.png)
