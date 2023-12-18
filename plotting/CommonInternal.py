# @Author: lshuns
# @Date:   2021-04-01, 21:08:02
# @Last modified by:   lshuns
# @Last modified time: 2021-04-01, 21:29:42

### some internal functions used by main modules

import functools

import matplotlib.pyplot as plt

def _vhlines(vORh, lines, line_styles=None, line_colors=None, line_labels=None, line_widths=None, ax=plt):
    """
    Add vertical or horizontal lines to the main plots

    Parameters
    ----------
    vORh : {'v', 'h'}
        vertical line (v) or horizontal line (h)

    lines : array-like of floats
        where to place the lines (x-axis for vline, y-axis for hline)

    line_styles : array-like of linestyles, default: 'dashed'

    line_colors : array-like of colors, default: 'k'

    line_labels : array-like of strings, default: ''

    line_widths : array-like of floats, default: 1

    ax : matplotlib Axes object, default: matplotlib.pyplot

    Returns
    -------
        None
    """

    for i, line in enumerate(lines):

        if line_styles is not None:
            line_style = line_styles[i]
        else:
            line_style = '--'

        if line_colors is not None:
            line_color = line_colors[i]
        else:
            line_color = 'k'

        if line_labels is not None:
            line_label = line_labels[i]
        else:
            line_label = ''

        if line_widths is not None:
            line_width = line_widths[i]
        else:
            line_width = 1

        if vORh == 'v':
            ax.axvline(x=line, ls=line_style, label=line_label, color=line_color, linewidth=line_width)
        elif vORh == 'h':
            ax.axhline(y=line, ls=line_style, label=line_label, color=line_color, linewidth=line_width)
        else:
            raise Exception(f'Unsupported vORh value: {vORh}')
