# Plot Highlight
plot_highlight is a Python visualization library based on [seaborn](https://seaborn.pydata.org).

This liblary is inspired by [gghighlight](https://yutannihilation.github.io/gghighlight/) package in R.


# Installation
Use pip
```
pip install plot-highlight
```

# Usage
Draw seaborn charts, highlighting the specific items.

The following seaborn functions are supported.
- `sns.scatterplot`
- `sns.lineplot`
- `sns.histplot`

## 📊 Scatter plot with highlight
```python
import seaborn as sns
df = sns.load_dataset('tips')

import plot_highlight as phl
phl.scatterplot(data=df, x='total_bill', y='tip', hue='day', highlights=['Sat', 'Sun'])
```
![highlight-scatterplot-01](https://raw.githubusercontent.com/shiro46mt/plot-highlight/main/example/highlight-scatterplot-01.png)

## 📊 Line plot with highlight
```python
import seaborn as sns
df = sns.load_dataset('healthexp')

import plot_highlight as phl
phl.lineplot(data=df, x='Year', y='Life_Expectancy', hue='Country', highlights=['Japan', 'USA'])
```
![highlight-lineplot-01](https://raw.githubusercontent.com/shiro46mt/plot-highlight/main/example/highlight-lineplot-01.png)

## 📊 Histgram with highlight
```python
import seaborn as sns
df = sns.load_dataset('penguins')

import plot_highlight as phl
phl.histplot(data=df, x='flipper_length_mm', hue='species', highlights='Adelie')
```
![highlight-histplot-01](https://raw.githubusercontent.com/shiro46mt/plot-highlight/main/example/highlight-histplot-01.png)

# License
This software is released under the MIT License, see LICENSE.
