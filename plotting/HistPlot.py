# @Author: lshuns
# @Date:   2021-04-01, 21:04:38
# @Last modified by:   lshuns
# @Last modified time: 2024-12-20 18:15:24

### everything about histogram

__all__ = ["HistPlotFunc", "Hist2DPlotFunc", "HistPlotFunc_subplots", "Hist2DPlotFunc_subplots"]

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

def HistPlotFunc(outpath,
                paras, wgs, COLORs, LABELs,
                nbins, XRANGE, YRANGE=None,
                XLABEL=None, YLABEL=None,
                DENSITY=False, HISTTYPE='step', STACKED=False,
                TITLE=None, xtick_min_label=True, ytick_min_label=True,
                xtick_spe=None, ytick_spe=None,
                vlines=None, vline_styles=None, vline_colors=None, vline_labels=None, vline_widths=None,
                hlines=None, hline_styles=None, hline_colors=None, hline_labels=None, hline_widths=None,
                xlog=False, ylog=False,
                loc_legend='best', 
                LABEL_position='inSub', LABEL_cols=1,
                font_size=12, usetex=False,
                cumulative=False, 
                FIGSIZE=[6.4, 4.8],
                LINEs=None, LINEWs=None,
                TIGHT=False,
                alpha=None,
                HISTTYPE_list=None):
    """
    Histogram plot for multiple parameters
    """

    # font size
    plt.rc('font', size=font_size)
    # tex
    plt.rcParams["text.usetex"] = usetex

    if outpath != 'show':
        backend_orig = plt.get_backend()
        plt.switch_backend("agg")

    if DENSITY and (wgs is not None):
        logger.warning('DENSITY and wgs are provided simultaneously!!!')

    if XRANGE is None:
        raise Exception('XRANGE cannot be None!')

    if xlog:
        bins = np.logspace(np.log10(XRANGE[0]), np.log10(XRANGE[1]), nbins)
    else:
        bins = np.linspace(XRANGE[0], XRANGE[1], nbins)

    fig, ax = plt.subplots(figsize=FIGSIZE)

    for i_para, para in enumerate(paras):
        if LINEs is not None:
            LINE = LINEs[i_para]
        else:
            LINE = None

        if LINEWs is not None:
            LW = LINEWs[i_para]
        else:
            LW = None

        if wgs is not None:
            wg = wgs[i_para]
        else:
            wg = None

        if LABELs is not None:
            LABEL = LABELs[i_para]
        else:
            LABEL = None

        if HISTTYPE_list is not None:
            HISTTYPE = HISTTYPE_list[i_para]

        _, _, handles = plt.hist(x=para, bins=bins, cumulative=cumulative,
                    range=XRANGE, density=DENSITY, weights=wg, 
                    color=COLORs[i_para], label=LABEL, 
                    histtype=HISTTYPE, stacked=STACKED,
                    ls=LINE, lw=LW, alpha=alpha)

    plt.xlim(XRANGE[0], XRANGE[1])
    if YRANGE is not None:
        plt.ylim(YRANGE[0], YRANGE[1])

    if xlog:
        plt.xscale('log')
    if ylog:
        plt.yscale('log')

    if vlines is not None:
        _vhlines('v', vlines, line_styles=vline_styles, line_colors=vline_colors, line_labels=vline_labels, line_widths=vline_widths)

    if hlines is not None:
        _vhlines('h', hlines, line_styles=hline_styles, line_colors=hline_colors, line_labels=hline_labels, line_widths=hline_widths)

    if xtick_min_label:
        if xlog:
            ax.xaxis.set_minor_locator(LogLocator(base=10.0, subs=None, numticks=10))
        else:
            ax.xaxis.set_minor_locator(AutoMinorLocator())
    if ytick_min_label:
        if ylog:
            ax.yaxis.set_minor_locator(LogLocator(base=10.0, subs=None, numticks=10))
        else:
            ax.yaxis.set_minor_locator(AutoMinorLocator())

    if xtick_spe is not None:
        plt.xticks(xtick_spe[0], xtick_spe[1])
    if ytick_spe is not None:
        plt.yticks(ytick_spe[0], ytick_spe[1])

    if (LABEL_position=='inSub') and (LABELs is not None):
        plt.legend(frameon=False, loc=loc_legend)
    elif (LABEL_position=='top') and (LABELs is not None):
        legend_handles = []
        for sublist in handles:
            legend_handles.append(sublist[0])
        fig.legend(legend_handles, LABELs, 
                loc = 'center', ncol=LABEL_cols,
                bbox_to_anchor=(0.5, 0.95), fancybox=True, shadow=True)

    plt.xlabel(XLABEL)
    plt.ylabel(YLABEL)
    if TITLE is not None:
        plt.title(TITLE)

    # avoid cutting in text
    if TIGHT:
        plt.tight_layout()

    if outpath == 'show':
        plt.show()
        plt.close()
    else:
        plt.savefig(outpath, dpi=300)
        plt.close()
        plt.switch_backend(backend_orig)
        print("Histogram plot saved as", outpath)

def Hist2DPlotFunc(outpath,
                x_val, y_val, wg,
                nbins, XRANGE=None, YRANGE=None,
                XLABEL=None, YLABEL=None, CBAR_LABEL=None,
                COLOR_MAP='Reds',
                DENSITY=False, count_scale=[None, None], count_log=False,
                TITLE=None, xtick_min_label=True, ytick_min_label=True,
                xtick_spe=None, ytick_spe=None,
                vlines=None, vline_styles=None, vline_colors=None, vline_labels=None, vline_widths=None,
                hlines=None, hline_styles=None, hline_colors=None, hline_labels=None, hline_widths=None,
                font_size=12, usetex=False, 
                FIGSIZE=[6.4, 4.8],
                TIGHT=False):
    """
    2D histogram plot
    """

    # font size
    plt.rc('font', size=font_size)
    # tex
    plt.rcParams["text.usetex"] = usetex

    if outpath != 'show':
        backend_orig = plt.get_backend()
        plt.switch_backend("agg")

    if DENSITY and (wg is not None):
        logger.warning('DENSITY and wgs are provided simultaneously!!!')

    if (XRANGE is not None) and (YRANGE is not None):
        SRANGE = [[XRANGE[0], XRANGE[1]], [YRANGE[0], YRANGE[1]]]
    else:
        SRANGE = None

    fig, ax = plt.subplots(figsize=FIGSIZE)
    if count_log:
        norm = mpl.colors.LogNorm(vmin=count_scale[0], vmax=count_scale[1])
    else:
        norm = mpl.colors.Normalize(vmin=count_scale[0], vmax=count_scale[1])
    h = plt.hist2d(x_val, y_val, bins=nbins, range=SRANGE, density=DENSITY, weights=wg, norm=norm, cmap=COLOR_MAP)
    cbar = plt.colorbar(h[3])

    if CBAR_LABEL is not None:
        cbar.ax.set_ylabel(CBAR_LABEL, rotation=270)

    if XRANGE is not None:
        plt.xlim(XRANGE[0], XRANGE[1])
    if YRANGE is not None:
        plt.ylim(YRANGE[0], YRANGE[1])

    if vlines is not None:
        _vhlines('v', vlines, line_styles=vline_styles, line_colors=vline_colors, line_labels=vline_labels, line_widths=vline_widths)

    if hlines is not None:
        _vhlines('h', hlines, line_styles=hline_styles, line_colors=hline_colors, line_labels=hline_labels, line_widths=hline_widths)

    if xtick_min_label:
        ax.xaxis.set_minor_locator(AutoMinorLocator())
    if ytick_min_label:
        ax.yaxis.set_minor_locator(AutoMinorLocator())

    if xtick_spe is not None:
        plt.xticks(xtick_spe[0], xtick_spe[1])
    if ytick_spe is not None:
        plt.yticks(ytick_spe[0], ytick_spe[1])

    plt.xlabel(XLABEL)
    plt.ylabel(YLABEL)
    if TITLE is not None:
        plt.title(TITLE)

    if TIGHT:
        plt.tight_layout()

    if outpath == 'show':
        plt.show()
        plt.close()
    else:
        plt.savefig(outpath, dpi=300)
        plt.close()
        plt.switch_backend(backend_orig)
        print("2D histogram plot saved as", outpath)

def HistPlotFunc_subplots(outpath, N_plots,
                            paras_list, wgs_list, COLORs_list, LABELs_list,
                            nbins_list, XRANGE, YRANGE=None,
                            LINEs_list=None, LINEWs_list=None,
                            subLABEL_list=None, subLABEL_locX=0.1, subLABEL_locY=0.8,
                            XLABEL=None, YLABEL=None,
                            DENSITY=False, HISTTYPE='step', STACKED=False,
                            TITLE=None, xtick_min_label=True, ytick_min_label=True,
                            xtick_spe=None, ytick_spe=None,
                            vlines_list=None, 
                            vline_styles_list=None, vline_colors_list=None, vline_labels_list=None, vline_widths_list=None,
                            hlines_list=None, 
                            hline_styles_list=None, hline_colors_list=None, hline_labels_list=None, hline_widths_list=None,
                            xlog=False, ylog=False,
                            loc_legend='best',
                            font_size=12, usetex=False,
                            LABEL_position='inSub', LABEL_position_SUBid=0,
                            LABEL_cols=1, 
                            FIGSIZE=[6.4, 4.8],
                            TIGHT=False,
                            HISTTYPEs_list=None,
                            shareX=True,
                            shareY=True,
                            XRANGE_list=None,
                            YRANGE_list=None):
    """
    Histogram plot for multiple subplots
    """

    # font size
    plt.rc('font', size=font_size)
    # tex
    plt.rcParams["text.usetex"] = usetex

    if outpath != 'show':
        backend_orig = plt.get_backend()
        plt.switch_backend("agg")

    N_rows = math.ceil(N_plots**0.5)
    N_cols = math.ceil(N_plots/N_rows)
    fig, axs = plt.subplots(N_rows, N_cols, sharex=shareX, sharey=shareY, figsize=FIGSIZE)
    if shareX and shareY:
        fig.subplots_adjust(hspace=0)
        fig.subplots_adjust(wspace=0)

    if DENSITY and (wgs_list is not None):
        logger.warning('DENSITY and wgs are provided simultaneously!!!')

    i_plot = 0
    for i_row in range(N_rows):
        for i_col in range(N_cols):
            if i_plot >= N_plots:
                if N_rows == 1:
                    axs[i_col].axis('off')
                elif N_cols == 1:
                    axs[i_row].axis('off')
                else:
                    axs[i_row, i_col].axis('off')
            else:
                if (N_rows==1) and (N_cols == 1):
                    ax = axs
                elif N_rows == 1:
                    ax = axs[i_col]
                elif N_cols == 1:
                    ax = axs[i_row]
                else:
                    ax = axs[i_row, i_col]

                paras = paras_list[i_plot]
                COLORs = COLORs_list[i_plot]
                if LABELs_list is not None:
                    LABELs = LABELs_list[i_plot]
                else:
                    LABELs = None

                if XRANGE_list is not None:
                    XRANGE = XRANGE_list[i_plot]

                if YRANGE_list is not None:
                    YRANGE = YRANGE_list[i_plot]

                if HISTTYPEs_list is not None:
                    HISTTYPEs = HISTTYPEs_list[i_plot]
                else:
                    HISTTYPEs = None

                if LINEs_list is not None:
                    LINEs = LINEs_list[i_plot]
                else:
                    LINEs = None

                if LINEWs_list is not None:
                    LINEWs = LINEWs_list[i_plot]
                else:
                    LINEWs = None

                nbins = nbins_list[i_plot]
                if wgs_list is not None:
                    wgs = wgs_list[i_plot]
                else:
                    wgs = None

                try:
                    vlines = vlines_list[i_plot]
                except TypeError:
                    vlines = None
                try:
                    vline_styles = vline_styles_list[i_plot]
                except TypeError:
                    vline_styles = None
                try:
                    vline_colors = vline_colors_list[i_plot]
                except TypeError:
                    vline_colors = None
                try:
                    vline_labels = vline_labels_list[i_plot]
                except TypeError:
                    vline_labels = None
                try:
                    vline_widths = vline_widths_list[i_plot]
                except TypeError:
                    vline_widths = None

                try:
                    hlines = hlines_list[i_plot]
                except TypeError:
                    hlines = None
                try:
                    hline_styles = hline_styles_list[i_plot]
                except TypeError:
                    hline_styles = None
                try:
                    hline_colors = hline_colors_list[i_plot]
                except TypeError:
                    hline_colors = None
                try:
                    hline_labels = hline_labels_list[i_plot]
                except TypeError:
                    hline_labels = None
                try:
                    hline_widths = hline_widths_list[i_plot]
                except TypeError:
                    hline_widths = None

                if xlog:
                    bins = np.logspace(np.log10(XRANGE[0]), np.log10(XRANGE[1]), nbins)
                else:
                    bins = np.linspace(XRANGE[0], XRANGE[1], nbins)

                for i_val_tmp, para_tmp in enumerate(paras):

                    if LINEs is not None:
                        LINE = LINEs[i_val_tmp]
                    else:
                        LINE = None

                    if LINEWs is not None:
                        LW = LINEWs[i_val_tmp]
                    else:
                        LW = None

                    if wgs is not None:
                        wg = wgs[i_val_tmp]
                    else:
                        wg = None

                    if LABELs is not None:
                        LABEL = LABELs[i_val_tmp]
                    else:
                        LABEL = None

                    if HISTTYPEs is not None:
                        HISTTYPE = HISTTYPEs[i_val_tmp]

                    ax.hist(x=para_tmp, 
                        bins=bins, range=XRANGE, density=DENSITY, 
                        weights=wg, color=COLORs[i_val_tmp], 
                        label=LABEL, histtype=HISTTYPE, 
                        stacked=STACKED,
                        ls=LINE, lw=LW)

                if (LABEL_position=='inSub') and (i_plot == LABEL_position_SUBid) and (LABELs is not None):
                    ax.legend(frameon=True, loc=loc_legend)

                if subLABEL_list is not None:
                    LABEL = subLABEL_list[i_plot]
                    ax.text(subLABEL_locX, subLABEL_locY, LABEL, transform=ax.transAxes)

                ax.set_xlim(XRANGE[0], XRANGE[1])
                if YRANGE is not None:
                    ax.set_ylim(YRANGE[0], YRANGE[1])

                if xlog:
                    ax.set_xscale('log')
                if ylog:
                    ax.set_yscale('log')

                if vlines is not None:
                    _vhlines('v', vlines, line_styles=vline_styles, line_colors=vline_colors, line_labels=vline_labels, line_widths=vline_widths, ax=ax)

                if hlines is not None:
                    _vhlines('h', hlines, line_styles=hline_styles, line_colors=hline_colors, line_labels=hline_labels, line_widths=hline_widths, ax=ax)

                if xtick_min_label:
                    if xlog:
                        ax.xaxis.set_minor_locator(LogLocator(base=10.0, subs=None, numticks=10))
                    else:
                        ax.xaxis.set_minor_locator(AutoMinorLocator())
                if ytick_min_label:
                    if ylog:
                        ax.yaxis.set_minor_locator(LogLocator(base=10.0, subs=None, numticks=10))
                    else:
                        ax.yaxis.set_minor_locator(AutoMinorLocator())

                if xtick_spe is not None:
                    plt.xticks(xtick_spe[0], xtick_spe[1])
                if ytick_spe is not None:
                    plt.yticks(ytick_spe[0], ytick_spe[1])

            i_plot +=1

    fig.text(0.5, 0.01, XLABEL, ha='center', va='bottom')
    fig.text(0.01, 0.5, YLABEL, ha='left', va='center', rotation='vertical')

    if (LABEL_position=='right') and (LABELs is not None):
        handles = [Rectangle((0,0),1,1,color='white', ec=c) for c in COLORs]
        fig.legend(handles, LABELs, 
                loc = 'upper right',
                bbox_to_anchor=(0.92, 0.35), fancybox=True, shadow=True)

    if (LABEL_position=='top') and (LABELs is not None):
        handles = [Rectangle((0,0),1,1,color='white', ec=c) for c in COLORs]
        fig.legend(handles, LABELs, 
                loc = 'center', ncol=LABEL_cols,
                bbox_to_anchor=(0.5, 0.95), fancybox=True, shadow=True)

    if TITLE is not None:
        fig.text(0.5, 0.90, TITLE, ha='center')

    if TIGHT:
        plt.tight_layout()

    if outpath == 'show':
        plt.show()
        plt.close()
    else:
        plt.savefig(outpath, dpi=300)
        plt.close()
        plt.switch_backend(backend_orig)
        print("Histogram plot saved as", outpath)

def Hist2DPlotFunc_subplots(outpath, N_plots,
                            x_val_list, y_val_list, wg_list,
                            nbins_list, XRANGE=None, YRANGE=None,
                            subLABEL_list=None, subLABEL_locX=0.1, subLABEL_locY=0.8,
                            XLABEL=None, YLABEL=None, CBAR_LABEL=None,
                            COLOR_MAP='Reds',
                            DENSITY=False, count_scale=[None, None], count_log=False,
                            TITLE=None, xtick_min_label=True, ytick_min_label=True,
                            xtick_spe=None, ytick_spe=None,
                            vlines=None, vline_styles=None, vline_colors=None, vline_labels=None, vline_widths=None,
                            hlines=None, hline_styles=None, hline_colors=None, hline_labels=None, hline_widths=None,
                            font_size=12, usetex=False, 
                            FIGSIZE=[6.4, 4.8],
                            TIGHT=False):
    """
    Histogram plot for multiple subplots
    """

    # font size
    plt.rc('font', size=font_size)
    # tex
    plt.rcParams["text.usetex"] = usetex

    if outpath != 'show':
        backend_orig = plt.get_backend()
        plt.switch_backend("agg")

    N_rows = math.ceil(N_plots**0.5)
    N_cols = math.ceil(N_plots/N_rows)
    fig, axs = plt.subplots(N_rows, N_cols, sharex=True, sharey=True, figsize=FIGSIZE)
    fig.subplots_adjust(hspace=0)
    fig.subplots_adjust(wspace=0)

    if DENSITY and (wg_list is not None):
        logger.warning('DENSITY and wgs are provided simultaneously!!!')

    if (XRANGE is not None) and (YRANGE is not None):
        SRANGE = [[XRANGE[0], XRANGE[1]], [YRANGE[0], YRANGE[1]]]
    else:
        SRANGE = None

    i_plot = 0
    for i_row in range(N_rows):
        for i_col in range(N_cols):
            if i_plot >= N_plots:
                if N_rows == 1:
                    axs[i_col].axis('off')
                elif N_cols == 1:
                    axs[i_row].axis('off')
                else:
                    axs[i_row, i_col].axis('off')
            else:
                if (N_rows==1) and (N_cols == 1):
                    ax = axs
                elif N_rows == 1:
                    ax = axs[i_col]
                elif N_cols == 1:
                    ax = axs[i_row]
                else:
                    ax = axs[i_row, i_col]

                x_val = x_val_list[i_plot]
                y_val = y_val_list[i_plot]
                nbins = nbins_list[i_plot]
                if wg_list is not None:
                    wg = wg_list[i_plot]
                else:
                    wg = None

                if count_log:
                    norm = mpl.colors.LogNorm(vmin=count_scale[0], vmax=count_scale[1])
                else:
                    norm = mpl.colors.Normalize(vmin=count_scale[0], vmax=count_scale[1])
                h = ax.hist2d(x_val, y_val, bins=nbins, range=SRANGE, density=DENSITY, weights=wg, norm=norm, cmap=COLOR_MAP)
    
                if subLABEL_list is not None:
                    LABEL = subLABEL_list[i_plot]
                    ax.text(subLABEL_locX, subLABEL_locY, LABEL, transform=ax.transAxes)

                if XRANGE is not None:
                    ax.set_xlim(XRANGE[0], XRANGE[1])
                if YRANGE is not None:
                    ax.set_ylim(YRANGE[0], YRANGE[1])

                if vlines is not None:
                    _vhlines('v', vlines, line_styles=vline_styles, line_colors=vline_colors, line_labels=vline_labels, line_widths=vline_widths, ax=ax)

                if hlines is not None:
                    _vhlines('h', hlines, line_styles=hline_styles, line_colors=hline_colors, line_labels=hline_labels, line_widths=hline_widths, ax=ax)

                if xtick_min_label:
                    ax.xaxis.set_minor_locator(AutoMinorLocator())
                if ytick_min_label:
                    ax.yaxis.set_minor_locator(AutoMinorLocator())

                if xtick_spe is not None:
                    plt.xticks(xtick_spe[0], xtick_spe[1])
                if ytick_spe is not None:
                    plt.yticks(ytick_spe[0], ytick_spe[1])

            i_plot +=1

    fig.text(0.5, 0.01, XLABEL, ha='center', va='bottom')
    fig.text(0.01, 0.5, YLABEL, ha='left', va='center', rotation='vertical')

    if TITLE is not None:
        fig.text(0.5, 0.90, TITLE, ha='center')

    cbar = fig.colorbar(h[3], ax=axs, location='right')
    if CBAR_LABEL is not None:
        cbar.ax.set_ylabel(CBAR_LABEL, rotation=270)

    if TIGHT:
        plt.tight_layout()

    if outpath == 'show':
        plt.show()
        plt.close()
    else:
        plt.savefig(outpath, dpi=300)
        plt.close()
        plt.switch_backend(backend_orig)
        print("2D histogram plot saved as", outpath)