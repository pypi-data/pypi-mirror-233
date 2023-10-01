import warnings
from collections.abc import Iterable
from math import log

import matplotlib.pyplot as plt
import seaborn as sns


def _highlightplot(func, data, hue, highlights, bg_color='gray', **kwargs):
    """Draw seaborn chart, highlighting the specific items.

    Args:
        func (functions of `seaborn`):
            Plotting function defined in `seaborn` function interface.
        data (`pandas.DataFrame`):
            Input data should be a long form.
        hue (keys in `data`):
            Grouping variable that will produce points with different colors. Can be either categorical or numeric, although color mapping will behave differently in latter case.
        highlights (str / vector of str):
            Specify the highlighted items for categorical levels of the `hue` semantic.
        bg_color (str, optional):
            Colors of the non-highlighted markers.
            Defaults to 'gray'.

    Returns:
        `matplotlib.axes.Axes`: The matplotlib axes containing the plot.
    """

    if isinstance(highlights, (str, int)):
        data_hl = data[data[hue] == highlights].copy()
        data_bg = data[data[hue] != highlights].copy()
    elif isinstance(highlights, Iterable):
        data_hl = data[data[hue].isin(highlights)].copy()
        data_bg = data[~(data[hue].isin(highlights))].copy()
    else:
        assert False, '`highlight` must be str or vector of str'

    try:
        data_hl[hue] = data_hl[hue].cat.remove_unused_categories()
        data_bg[hue] = data_bg[hue].cat.remove_unused_categories()
    except AttributeError:
        pass

    # plot back-ground items
    n_categ_bg = int(data_bg[hue].nunique())
    kwargs_bg = kwargs.copy()
    kwargs_bg['palette'] = [bg_color] * n_categ_bg
    kwargs_bg['alpha'] = kwargs_bg.get('alpha', 1) * 0.5
    kwargs_bg['legend'] = False
    func(data=data_bg, hue=hue, **kwargs_bg)

    # plot highlighted items
    func(data=data_hl, hue=hue, **kwargs)

    return plt.gca()


def scatterplot(data, *, hue=None, highlights=None, **kwargs):
    """Plot `sns.scatterplot` with highlights.

    Args:
        highlights (str / vector of str):
            Specify the highlighted items for categorical levels of the `hue` semantic.
            When not specified, all the hue categories will be highlighted

        Other args:
            See `sns.scatterplot`

    Returns:
        `matplotlib.axes.Axes`: The matplotlib axes containing the plot.
    """
    return _highlightplot(sns.scatterplot, data, hue, highlights, **kwargs)


def lineplot(data, *, hue=None, highlights=None, **kwargs):
    """Plot `sns.lineplot` with highlights.

    Args:
        highlights (str / vector of str):
            Specify the highlighted items for categorical levels of the `hue` semantic.
            When not specified, all the hue categories will be highlighted

        Other args:
            See `sns.lineplot`

    Returns:
        `matplotlib.axes.Axes`: The matplotlib axes containing the plot.
    """
    return _highlightplot(sns.lineplot, data, hue, highlights, **kwargs)


def histplot(data, *, hue=None, highlights=None, **kwargs):
    """Plot `sns.histplot` with highlights.

    Args:
        highlights (str / vector of str):
            Specify the highlighted items for categorical levels of the `hue` semantic.
            When not specified, all the hue categories will be highlighted

        Other args:
            See `sns.histplot`

    Returns:
        `matplotlib.axes.Axes`: The matplotlib axes containing the plot.
    """
    if 'binrange' not in kwargs:
        x = kwargs.get('x', kwargs.get('y', None))
        assert x is not None, 'You should pass either `x` or `y` variable.'

        if kwargs.get('log_scale', False):
            base = float(kwargs.get('log_scale'))
            if base == 1:
                base = 10
            kwargs['binrange'] = (log(data[x].min(), base), log(data[x].max(), base))
        else:
            kwargs['binrange'] = (data[x].min(), data[x].max())

    if 'bins' not in kwargs and 'binwidth' not in kwargs:
        kwargs['bins'] = 10
        msg = (
            "Either `bins` or `binwidth` should be set to align bin edges. "
            "Setting `bins=10`, but you will likely want to adjust."
        )
        warnings.warn(msg)

    return _highlightplot(sns.histplot, data, hue, highlights, **kwargs)
