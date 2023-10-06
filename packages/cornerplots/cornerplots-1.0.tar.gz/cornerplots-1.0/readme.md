# Cornerplots

Simple library to create corner plots in `matplotlib`. Corner plots provide a simple way to visualize multidimensional data, with each dimension plotted against every other dimension. The main goal is to let the user specify data and/or model predictions in arbitrary subsets of the multi-dimensional space and let the code take care of where to plot these values. Originally inspired by [corner.py](https://github.com/dfm/corner.py).

## Simple example

You might have one set of (*w*, *x*, *y*) data, another set of (*x*, *y*, *z*) data, and a model predicting (*w*, *x*, *y*, *z*) trajectories.

```py
import numpy as np

t = np.linspace(0, 1)
model = dict(
    w = 3 * t + 1,
    x = 5 * t,
    y = 7 * t**.5,
    z = 3 * t**1.5,
    )

red_data = dict(
    w = np.array([1, 2, 3, 4]),
    x = np.array([0, 2, 4, 5]),
    y = np.array([1, 4, 6, 8]),
    )

blue_data = dict(
    x = np.array([1, 2, 5]),
    y = np.array([3, 5, 7]),
    z = np.array([0, 1, 3]),
    )
```

In that case, you could plot everything by simply calling:



```py
from cornerplots import Cornerplots
import matplotlib.pyplot as ppl

fig = ppl.figure(figsize = (5,5))

cp = Cornerplots(
    fields = ['w', 'x', 'y', 'z'],
    labels = ['W-value', 'X-value', 'Y-value', 'Z-value'],
    grid_kwargs = {'alpha': 0.25, 'lw': 0.7},
    )

cp.plot(model,     'k-', lw = 1, dashes = (6,2,2,2), label = 'model')
cp.plot(red_data,  'ws', mec = 'r', mew = 1, ms = 5, label = 'red data')
cp.plot(blue_data, 'wD', mec = 'b', mew = 1, ms = 5, label = 'blue data')

cp.legend()

ppl.savefig('example.png')
```


<div align="center">
<img src="example.png">
</div>