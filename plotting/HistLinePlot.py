# -*- coding: utf-8 -*-
# @Author: lshuns
# @Date:   2022-04-21 14:16:38
# @Last Modified by:   lshuns
# @Last Modified time: 2024-05-06 18:07:07

### everything about histogram + line plots

__all__ = ["HistErrorPlotFunc", "HistTwinxErrorPlotFunc"]

import math
import logging

import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.rcParams['xtick.direction'] = 'in'
mpl.rcParams['ytick.direction'] = 'in'
mpl.rcParams['xtick.top'] = True
mpl.rcParams['ytick.right'] = True
plt.rcParams['font.family'] = 'serif'

from matplotlib.ticker import AutoMinorLocator, LogLocator
from matplotlib.patches import Rectangle

from .CommonInternal import _vhlines

logging.basicConfig(format='%(name)s : %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def HistErrorPlotFunc(outpath,
                paras_hist, wgs_hist, COLORs_hist, 
                xvals_error, yvals_error, COLORs_error,
                LABELs_hist=None, nbins_hist=60, cumulative=False,
                LABELs_error=None,
                xerrs_error=None, yerrs_error=None,
                LINEs=None, LINEWs=None, POINTs=None, POINTSs=None, ERRORSIZEs=None,
                XRANGE=None, YRANGE_hist=None, YRANGE_error=None,
                XLABEL=None, YLABEL_hist=None, YLABEL_error=None,
                DENSITY=False, HISTTYPE='step', STACKED=False,
                TITLE=None, 
                xtick_min_label=True, ytick_min_label=True,
                xtick_spe=None,
                vlines=None, vline_styles=None, vline_colors=None, vline_labels=None, vline_widths=None,
                hlines=None, hline_styles=None, hline_colors=None, hline_labels=None, hline_widths=None,
                xlog=False, invertX=False, 
                ylog_hist=False, ylog_error=False, 
                invertY_hist=False, invertY_error=False, 
                loc_legend='best', frameon_legend=False,
                font_size=12, usetex=False):
    """
    Histogram and line plot for multiple parameters
    """

    # font size
    plt.rc('font', size=font_size)
    # tex
    plt.rcParams["text.usetex"] = usetex

    if outpath != 'show':
        backend_orig = plt.get_backend()
        plt.switch_backend("agg")

    if DENSITY and (wgs_hist is not None):
        logger.warning('DENSITY and wgs are provided simultaneously!!!')

    # definitions for the axes
    left, width = 0.1, 0.8
    bottom, height, spacing = 0.1, 0.65, 0.01
    rect_scatter = [left, bottom, width, height]
    rect_histx = [left, bottom + height + spacing, width, 0.14]

    # start with a square Figure
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_axes(rect_scatter)
    ax_hist = fig.add_axes(rect_histx, sharex=ax)

    ### >>>>>>>>>> for histogram plots
    if XRANGE is not None:
        bin_min = XRANGE[0]
        bin_max = XRANGE[1]
    else:
        bin_min = np.amin(paras_hist)
        bin_max = np.amax(paras_hist)
    if xlog:
        logbins = np.logspace(np.log10(bin_min), np.log10(bin_max), nbins_hist)
        ax_hist.hist(x=paras_hist, bins=logbins, cumulative=cumulative,
                    density=DENSITY, weights=wgs_hist, 
                    color=COLORs_hist, label=LABELs_hist, histtype=HISTTYPE, stacked=STACKED)
    else:
        ax_hist.hist(x=paras_hist, bins=nbins_hist, cumulative=cumulative, 
                    range=[bin_min, bin_max], density=DENSITY, 
                    weights=wgs_hist, color=COLORs_hist, label=LABELs_hist, histtype=HISTTYPE, stacked=STACKED)

    if YRANGE_hist is not None:
        ax_hist.set_ylim(YRANGE_hist[0], YRANGE_hist[1])

    if ylog_hist:
        ax_hist.set_yscale('log')

    if ytick_min_label:
        if ylog_hist:
            ax_hist.yaxis.set_minor_locator(LogLocator(base=10.0, subs=None, numticks=10))
        else:
            ax_hist.yaxis.set_minor_locator(AutoMinorLocator())

    if invertY_hist:
        ax_hist.invert_yaxis()

    ax_hist.set_ylabel(YLABEL_hist)

    ax_hist.tick_params(labelbottom=False)

    if (LABELs_hist is not None):
        ax_hist.legend(frameon=frameon_legend, loc=loc_legend)

    ### >>>>>>>>>> for error bar plots
    for i, xvl in enumerate(xvals_error):
        yvl = yvals_error[i]
        if yerrs_error is not None:
            yerr = yerrs_error[i]
            if yerr is not None:
                yerr = np.array(yerr)
                yerr = np.vstack([yerr[0], yerr[1]])
        else:
            yerr = None

        if xerrs_error is not None:
            xerr = xerrs_error[i]
            if xerr is not None:
                xerr = np.array(xerr)
                xerr = np.vstack([xerr[0], xerr[1]])
        else:
            xerr = None

        CR = COLORs_error[i]

        if LABELs_error is not None:
            LAB = LABELs_error[i]
        else:
            LAB = None

        if LINEs is not None:
            LN = LINEs[i]
        else:
            LN = '--'
        if LINEWs is not None:
            LW = LINEWs[i]
        else:
            LW = 1

        if POINTs is not None:
            PI = POINTs[i]
        else:
            PI = 'o'
        if POINTSs is not None:
            MS = POINTSs[i]
        else:
            MS = 2

        if ERRORSIZEs is not None:
            ERRORSIZE = ERRORSIZEs[i]
        else:
            ERRORSIZE = 2

        ax.errorbar(xvl, yvl, xerr=xerr, yerr=yerr, 
            color=CR, label=LAB, linestyle=LN, linewidth=LW, marker=PI, markersize=MS, capsize=ERRORSIZE)

    if YRANGE_error is not None:
        ax.set_ylim(YRANGE_error[0], YRANGE_error[1])

    if ylog_error:
        ax.set_yscale('log')

    if ytick_min_label:
        if ylog_error:
            ax.yaxis.set_minor_locator(LogLocator(base=10.0, subs=None, numticks=10))
        else:
            ax.yaxis.set_minor_locator(AutoMinorLocator())

    if invertY_error:
        ax.invert_yaxis()

    ax.set_ylabel(YLABEL_error)

    if (LABELs_error is not None):
        ax.legend(frameon=frameon_legend, loc=loc_legend)

    ### >>>>>>>>>> common
    if XRANGE is not None:
        plt.xlim(XRANGE[0], XRANGE[1])

    if xlog:
        plt.xscale('log')

    if vlines is not None:
        _vhlines('v', vlines, line_styles=vline_styles, line_colors=vline_colors, line_labels=vline_labels, line_widths=vline_widths, ax=ax)

    if hlines is not None:
        _vhlines('h', hlines, line_styles=hline_styles, line_colors=hline_colors, line_labels=hline_labels, line_widths=hline_widths, ax=ax)

    if xtick_min_label:
        if xlog:
            ax.xaxis.set_minor_locator(LogLocator(base=10.0, subs=None, numticks=10))
        else:
            ax.xaxis.set_minor_locator(AutoMinorLocator())

    if xtick_spe is not None:
        plt.xticks(xtick_spe[0], xtick_spe[1])

    if invertX:
        plt.gca().invert_xaxis()

    ax.set_xlabel(XLABEL)
    if TITLE is not None:
        plt.title(TITLE)

    if outpath == 'show':
        plt.show()
        plt.close()
    else:
        plt.savefig(outpath, dpi=300)
        plt.close()
        plt.switch_backend(backend_orig)
        print("Histogram plot saved as", outpath)


def HistTwinxErrorPlotFunc(outpath,
                paras_hist, wgs_hist, COLORs_hist, 
                xvals_error_left, yvals_error_left, COLORs_error_left,
                xvals_error_right, yvals_error_right, COLORs_error_right,
                LABELs_hist=None, nbins_hist=60, cumulative=False,
                LABELs_error_left=None, LABELs_error_right=None,
                xerrs_error_left=None, xerrs_error_right=None, 
                yerrs_error_left=None, yerrs_error_right=None,
                LINEs_left=None, LINEWs_left=None, POINTs_left=None, POINTSs_left=None, ERRORSIZEs_left=None,
                LINEs_right=None, LINEWs_right=None, POINTs_right=None, POINTSs_right=None, ERRORSIZEs_right=None,
                XRANGE=None, YRANGE_hist=None, YRANGE_error_left=None, YRANGE_error_right=None, 
                XLABEL=None, YLABEL_hist=None, YLABEL_error_left=None, YLABEL_error_right=None,
                DENSITY=False, HISTTYPE='step', STACKED=False,
                TITLE=None, 
                xtick_min_label=True, ytick_min_label=True,
                xtick_spe=None,
                vlines=None, vline_styles=None, vline_colors=None, vline_labels=None, vline_widths=None,
                hlines=None, hline_styles=None, hline_colors=None, hline_labels=None, hline_widths=None,
                xlog=False, invertX=False, 
                ylog_hist=False, ylog_error_left=False, ylog_error_right=False,
                invertY_hist=False, invertY_error_left=False, invertY_error_right=False, 
                loc_legend='best', frameon_legend=False,
                font_size=12, usetex=False):
    """
    Histogram and line plot for multiple parameters
    """

    # font size
    plt.rc('font', size=font_size)
    # tex
    plt.rcParams["text.usetex"] = usetex

    if outpath != 'show':
        backend_orig = plt.get_backend()
        plt.switch_backend("agg")

    if DENSITY and (wgs_hist is not None):
        logger.warning('DENSITY and wgs are provided simultaneously!!!')

    # definitions for the axes
    left, width = 0.1, 0.8
    bottom, height, spacing = 0.1, 0.65, 0.01
    rect_scatter = [left, bottom, width, height]
    rect_histx = [left, bottom + height + spacing, width, 0.14]

    # start with a square Figure
    fig = plt.figure(figsize=(8, 8))
    ax_left = fig.add_axes(rect_scatter)
    ax_right = ax_left.twinx()
    ax_hist = fig.add_axes(rect_histx, sharex=ax_left)

    ### >>>>>>>>>> for histogram plots
    if XRANGE is not None:
        bin_min = XRANGE[0]
        bin_max = XRANGE[1]
    else:
        bin_min = np.amin(paras_hist)
        bin_max = np.amax(paras_hist)
    if xlog:
        logbins = np.logspace(np.log10(bin_min), np.log10(bin_max), nbins_hist)
        ax_hist.hist(x=paras_hist, bins=logbins, cumulative=cumulative,
                    density=DENSITY, weights=wgs_hist, 
                    color=COLORs_hist, label=LABELs_hist, histtype=HISTTYPE, stacked=STACKED)
    else:
        ax_hist.hist(x=paras_hist, bins=nbins_hist, cumulative=cumulative, 
                    range=[bin_min, bin_max], density=DENSITY, 
                    weights=wgs_hist, color=COLORs_hist, label=LABELs_hist, histtype=HISTTYPE, stacked=STACKED)

    if YRANGE_hist is not None:
        ax_hist.set_ylim(YRANGE_hist[0], YRANGE_hist[1])

    if ylog_hist:
        ax_hist.set_yscale('log')

    if ytick_min_label:
        if ylog_hist:
            ax_hist.yaxis.set_minor_locator(LogLocator(base=10.0, subs=None, numticks=10))
        else:
            ax_hist.yaxis.set_minor_locator(AutoMinorLocator())

    if invertY_hist:
        ax_hist.invert_yaxis()

    ax_hist.set_ylabel(YLABEL_hist)

    ax_hist.tick_params(labelbottom=False)

    if (LABELs_hist is not None):
        ax_hist.legend(frameon=frameon_legend, loc=loc_legend)

    ### >>>>>>>>>> for error bar plots
    ###### the left
    for i, xvl in enumerate(xvals_error_left):
        yvl = yvals_error_left[i]
        if yerrs_error_left is not None:
            yerr = yerrs_error_left[i]
            if yerr is not None:
                yerr = np.array(yerr)
                yerr = np.vstack([yerr[0], yerr[1]])
        else:
            yerr = None

        if xerrs_error_left is not None:
            xerr = xerrs_error_left[i]
            if xerr is not None:
                xerr = np.array(xerr)
                xerr = np.vstack([xerr[0], xerr[1]])
        else:
            xerr = None

        CR = COLORs_error_left[i]

        if LABELs_error_left is not None:
            LAB = LABELs_error_left[i]
        else:
            LAB = None

        if LINEs_left is not None:
            LN = LINEs_left[i]
        else:
            LN = '--'
        if LINEWs_left is not None:
            LW = LINEWs_left[i]
        else:
            LW = 1

        if POINTs_left is not None:
            PI = POINTs_left[i]
        else:
            PI = 'o'
        if POINTSs_left is not None:
            MS = POINTSs_left[i]
        else:
            MS = 2

        if ERRORSIZEs_left is not None:
            ERRORSIZE = ERRORSIZEs_left[i]
        else:
            ERRORSIZE = 2

        ax_left.errorbar(xvl, yvl, xerr=xerr, yerr=yerr, 
            color=CR, label=LAB, linestyle=LN, linewidth=LW, marker=PI, markersize=MS, capsize=ERRORSIZE)

    if YRANGE_error_left is not None:
        ax_left.set_ylim(YRANGE_error_left[0], YRANGE_error_left[1])

    if ylog_error_left:
        ax_left.set_yscale('log')

    if ytick_min_label:
        if ylog_error_left:
            ax_left.yaxis.set_minor_locator(LogLocator(base=10.0, subs=None, numticks=10))
        else:
            ax_left.yaxis.set_minor_locator(AutoMinorLocator())

    if invertY_error_left:
        ax_left.invert_yaxis()

    ax_left.set_ylabel(YLABEL_error_left)

    if (LABELs_error_left is not None):
        ax_left.legend(frameon=frameon_legend, loc=loc_legend)

    ###### the right
    for i, xvl in enumerate(xvals_error_right):
        yvl = yvals_error_right[i]
        if yerrs_error_right is not None:
            yerr = yerrs_error_right[i]
            if yerr is not None:
                yerr = np.array(yerr)
                yerr = np.vstack([yerr[0], yerr[1]])
        else:
            yerr = None

        if xerrs_error_right is not None:
            xerr = xerrs_error_right[i]
            if xerr is not None:
                xerr = np.array(xerr)
                xerr = np.vstack([xerr[0], xerr[1]])
        else:
            xerr = None

        CR = COLORs_error_right[i]

        if LABELs_error_right is not None:
            LAB = LABELs_error_right[i]
        else:
            LAB = None

        if LINEs_right is not None:
            LN = LINEs_right[i]
        else:
            LN = '--'
        if LINEWs_right is not None:
            LW = LINEWs_right[i]
        else:
            LW = 1

        if POINTs_right is not None:
            PI = POINTs_right[i]
        else:
            PI = 'o'
        if POINTSs_right is not None:
            MS = POINTSs_right[i]
        else:
            MS = 2

        if ERRORSIZEs_right is not None:
            ERRORSIZE = ERRORSIZEs_right[i]
        else:
            ERRORSIZE = 2

        ax_right.errorbar(xvl, yvl, xerr=xerr, yerr=yerr, 
            color=CR, label=LAB, linestyle=LN, linewidth=LW, marker=PI, markersize=MS, capsize=ERRORSIZE)

    if YRANGE_error_right is not None:
        ax_right.set_ylim(YRANGE_error_right[0], YRANGE_error_right[1])

    if ylog_error_right:
        ax_right.set_yscale('log')

    if ytick_min_label:
        if ylog_error_right:
            ax_right.yaxis.set_minor_locator(LogLocator(base=10.0, subs=None, numticks=10))
        else:
            ax_right.yaxis.set_minor_locator(AutoMinorLocator())

    if invertY_error_right:
        ax_right.invert_yaxis()

    ax_right.set_ylabel(YLABEL_error_right)

    if (LABELs_error_right is not None):
        ax_right.legend(frameon=frameon_legend, loc=loc_legend)

    ### >>>>>>>>>> common
    if XRANGE is not None:
        plt.xlim(XRANGE[0], XRANGE[1])

    if xlog:
        plt.xscale('log')

    if vlines is not None:
        _vhlines('v', vlines, line_styles=vline_styles, line_colors=vline_colors, line_labels=vline_labels, line_widths=vline_widths, ax=ax_left)

    if hlines is not None:
        _vhlines('h', hlines, line_styles=hline_styles, line_colors=hline_colors, line_labels=hline_labels, line_widths=hline_widths, ax=ax_left)

    if xtick_min_label:
        if xlog:
            ax_left.xaxis.set_minor_locator(LogLocator(base=10.0, subs=None, numticks=10))
        else:
            ax_left.xaxis.set_minor_locator(AutoMinorLocator())

    if xtick_spe is not None:
        plt.xticks(xtick_spe[0], xtick_spe[1])

    if invertX:
        plt.gca().invert_xaxis()

    ax_left.set_xlabel(XLABEL)
    if TITLE is not None:
        plt.title(TITLE)

    if outpath == 'show':
        plt.show()
        plt.close()
    else:
        plt.savefig(outpath, dpi=300)
        plt.close()
        plt.switch_backend(backend_orig)
        print("Histogram plot saved as", outpath)
