# @Author: lshuns
# @Date:   2021-04-05, 21:44:40
# @Last modified by:   lshuns
# @Last modified time: 2024-12-20 18:16:30

### everything about Line/Point plot

__all__ = ["LinePlotFunc", "LinePlotFunc_subplots", "ErrorPlotFunc", "ErrorPlotFunc_subplots",
            "ScatterPlotFunc", "ErrorPlotFunc_2sub_shareX"]

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

from matplotlib.ticker import AutoMinorLocator, LogLocator, NullFormatter, NullLocator

from .CommonInternal import _vhlines

logging.basicConfig(format='%(name)s : %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def LinePlotFunc(outpath,
                xvals, yvals,
                COLORs, LABELs=None, LINEs=None, LINEWs=None, POINTs=None, POINTSs=None, fillstyles=None,
                XRANGE=None, YRANGE=None,
                XLABEL=None, YLABEL=None, TITLE=None,
                xtick_min_label=True, xtick_spe=None, ytick_min_label=True, ytick_spe=None,
                vlines=None, vline_styles=None, vline_colors=None, vline_labels=None, vline_widths=None,
                hlines=None, hline_styles=None, hline_colors=None, hline_labels=None, hline_widths=None,
                xlog=False, invertX=False, ylog=False, invertY=False, 
                loc_legend='best', legend_frame=False,
                font_size=12, usetex=False,
                FIGSIZE=[6.4, 4.8],
                texPacks=None):
    """
    Line plot for multiple parameters
    """

    # font size
    plt.rc('font', size=font_size)
    # tex
    plt.rcParams["text.usetex"] = usetex
    if texPacks is not None:
        for texPack in texPacks:
            plt.rcParams['text.latex.preamble']=texPack

    if outpath != 'show':
        backend_orig = plt.get_backend()
        plt.switch_backend("agg")

    fig, ax = plt.subplots(figsize=FIGSIZE)
    for i, xvl in enumerate(xvals):
        yvl = yvals[i]

        CR = COLORs[i]

        if LABELs is not None:
            LAB = LABELs[i]
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
        if fillstyles is not None:
            fillstyle = fillstyles[i]
        else:
            fillstyle = 'full'

        plt.plot(xvl, yvl, color=CR, label=LAB, linestyle=LN, linewidth=LW, marker=PI, markersize=MS, fillstyle=fillstyle)

    if XRANGE is not None:
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

    if LABELs is not None:
        plt.legend(frameon=legend_frame, loc=loc_legend)

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

    if invertX:
        plt.gca().invert_xaxis()
    if invertY:
        plt.gca().invert_yaxis()

    plt.xlabel(XLABEL)
    plt.ylabel(YLABEL)
    if TITLE is not None:
        plt.title(TITLE)

    plt.tight_layout()

    if outpath=='show':
        plt.show()
        plt.close()
    else:
        plt.savefig(outpath, dpi=300)
        plt.close()
        plt.switch_backend(backend_orig)
        print("Line plot saved as", outpath)

def LinePlotFunc_subplots(outpath, N_plots,
                            xvals_list, yvals_list,
                            COLORs_list, LABELs_list=None, LINEs_list=None, LINEWs_list=None, POINTs_list=None, POINTSs_list=None, fillstyles_list=None,
                            subLABEL_list=None, subLABEL_locX=0.1, subLABEL_locY=0.8,
                            XRANGE=None, YRANGE=None,
                            XLABEL=None, YLABEL=None, TITLE=None,
                            xtick_min_label=True, xtick_spe=None, ytick_min_label=True, ytick_spe=None,
                            vlines=None, vline_styles=None, vline_colors=None, vline_labels=None, vline_widths=None,
                            hlines=None, hline_styles=None, hline_colors=None, hline_labels=None, hline_widths=None,
                            xlog=False, invertX=False, ylog=False, invertY=False, 
                            loc_legend='best', legend_frame=False,
                            font_size=12, usetex=False,
                            LABEL_position='inSub', LABEL_position_SUBid=0,
                            LABEL_cols=1,
                            FIGSIZE=[6.4, 4.8],
                            TIGHT=False):
    """
    Line plot for multiple subplots
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

    i_plot = 0
    handles = []
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

                xvals = xvals_list[i_plot]
                yvals = yvals_list[i_plot]

                COLORs = COLORs_list[i_plot]

                if LABELs_list is not None:
                    LABELs = LABELs_list[i_plot]
                else:
                    LABELs = None

                if LINEs_list is not None:
                    LINEs = LINEs_list[i_plot]
                else:
                    LINEs = None
                if LINEWs_list is not None:
                    LINEWs = LINEWs_list[i_plot]
                else:
                    LINEWs = None

                if POINTs_list is not None:
                    POINTs = POINTs_list[i_plot]
                else:
                    POINTs = None
                if POINTSs_list is not None:
                    POINTSs = POINTSs_list[i_plot]
                else:
                    POINTSs = None
                if fillstyles_list is not None:
                    fillstyles = fillstyles_list[i_plot]
                else:
                    fillstyles = None

                for i, xvl in enumerate(xvals):
                    yvl = yvals[i]

                    CR = COLORs[i]

                    if LABELs is not None:
                        LAB = LABELs[i]
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
                    if fillstyles is not None:
                        fillstyle = fillstyles[i]
                    else:
                        fillstyle = 'full'

                    tmp = ax.plot(xvl, yvl, color=CR, label=LAB, linestyle=LN, linewidth=LW, marker=PI, markersize=MS, fillstyle=fillstyle)
                    if (LABEL_position!='inSub') and (i_plot==0):
                        handles.append(tmp[0])
                    del tmp

                if (LABEL_position=='inSub') and (LABELs is not None) and (i_plot == LABEL_position_SUBid):
                    ax.legend(frameon=legend_frame, loc=loc_legend)

                if subLABEL_list is not None:
                    LABEL = subLABEL_list[i_plot]
                    ax.text(subLABEL_locX, subLABEL_locY, LABEL, transform=ax.transAxes)

                if XRANGE is not None:
                    ax.set_xlim(XRANGE[0], XRANGE[1])
                if YRANGE is not None:
                    ax.set_ylim(YRANGE[0], YRANGE[1])

                if xlog:
                    ax.set_xscale('log')
                    ax.xaxis.set_minor_formatter(NullFormatter())
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

                if invertY:
                    plt.gca().invert_yaxis()
                if invertX:
                    plt.gca().invert_xaxis()

            i_plot +=1

    fig.text(0.5, 0.01, XLABEL, ha='center', va='bottom')
    fig.text(0.01, 0.5, YLABEL, ha='left', va='center', rotation='vertical')

    if TITLE is not None:
        fig.text(0.5, 0.90, TITLE, ha='center')

    if (LABEL_position=='right') and (LABELs is not None):
        fig.legend(handles, LABELs, 
                loc = 'upper right',
                bbox_to_anchor=(0.92, 0.35), fancybox=True, shadow=True)

    if (LABEL_position=='top') and (LABELs is not None):
        fig.legend(handles, LABELs, 
                loc = 'center', ncol=LABEL_cols,
                bbox_to_anchor=(0.5, 0.95), fancybox=True, shadow=True)

    if TIGHT:
        plt.tight_layout()

    if outpath == 'show':
        plt.show()
        plt.close()
    else:
        plt.savefig(outpath, dpi=300)
        plt.close()
        plt.switch_backend(backend_orig)
        print("Line plot saved as", outpath)

def ErrorPlotFunc(outpath,
                xvals, yvals, yerrs,
                COLORs, LABELs=None, LINEs=None, LINEWs=None, POINTs=None, POINTSs=None, ERRORSIZEs=None,
                XRANGE=None, YRANGE=None,
                XLABEL=None, YLABEL=None, TITLE=None,
                xtick_min_label=True, xtick_spe=None, ytick_min_label=True, ytick_spe=None,
                vlines=None, vline_styles=None, vline_colors=None, vline_labels=None, vline_widths=None,
                hlines=None, hline_styles=None, hline_colors=None, hline_labels=None, hline_widths=None,
                xlog=False, invertX=False, ylog=False, invertY=False, 
                loc_legend='best', legend_frame=False, frame_alpha=0.8,
                fill_between_xs=None, 
                fill_between_yLows=None, fill_between_yHighs=None,
                fill_between_COLORs=None, fill_between_alphas=None,
                font_size=12, usetex=False,
                xerrs=None, 
                alpha_list = None, zorder_list = None,
                FIGSIZE=[6.4, 4.8],
                transparent=False,
                font_size_label=None):
    """
    Errorbar plot for multiple parameters
    """

    # font size
    plt.rc('font', size=font_size)
    if font_size_label is None:
        font_size_label = font_size
    # tex
    plt.rcParams["text.usetex"] = usetex

    if outpath != 'show':
        backend_orig = plt.get_backend()
        plt.switch_backend("agg")

    fig, ax = plt.subplots(figsize=FIGSIZE)
    for i, xvl in enumerate(xvals):
        yvl = yvals[i]
        if yerrs is not None:
            yerr = yerrs[i]
            if yerr is not None:
                yerr = np.array(yerr)
                yerr = np.vstack([yerr[0], yerr[1]])
        else:
            yerr = None

        if xerrs is not None:
            xerr = xerrs[i]
            if xerr is not None:
                xerr = np.array(xerr)
                xerr = np.vstack([xerr[0], xerr[1]])
        else:
            xerr = None

        CR = COLORs[i]

        if alpha_list is not None:
            alpha = alpha_list[i]
        else:
            alpha = None
        if zorder_list is not None:
            zorder = zorder_list[i]
        else:
            zorder = i + 1

        if LABELs is not None:
            LAB = LABELs[i]
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
            color=CR, label=LAB, linestyle=LN, linewidth=LW, marker=PI, markersize=MS, capsize=ERRORSIZE,
            alpha=alpha,
            zorder=zorder)

    if fill_between_xs is not None:
        for i_fill, fill_between_x in enumerate(fill_between_xs):
            ax.fill_between(fill_between_x, 
                        fill_between_yLows[i_fill], fill_between_yHighs[i_fill],
                        alpha=fill_between_alphas[i_fill],
                        color=fill_between_COLORs[i_fill])

    if XRANGE is not None:
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

    if LABELs is not None:
        plt.legend(frameon=legend_frame, framealpha=frame_alpha, loc=loc_legend, fontsize=font_size_label)

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

    if invertX:
        plt.gca().invert_xaxis()
    if invertY:
        plt.gca().invert_yaxis()

    plt.xlabel(XLABEL)
    plt.ylabel(YLABEL)
    if TITLE is not None:
        plt.title(TITLE)

    plt.tight_layout()

    if outpath=='show':
        plt.show()
        plt.close()
    else:
        plt.savefig(outpath, dpi=300, transparent=transparent)
        plt.close()
        plt.switch_backend(backend_orig)
        print("Errorbar plot saved in", outpath)

def ErrorPlotFunc_subplots(outpath, N_plots,
                            xvals_list, yvals_list, yerrs_list,
                            COLORs_list, LABELs_list=None, LINEs_list=None, LINEWs_list=None, POINTs_list=None, POINTSs_list=None, ERRORSIZEs_list=None,
                            subLABEL_list=None, subLABEL_locX=0.1, subLABEL_locY=0.8, subLABEL_bbox=None,
                            XRANGE=None, YRANGE=None,
                            XLABEL=None, YLABEL=None, TITLE=None,
                            xtick_min_label=True, xtick_spe=None, ytick_min_label=True, ytick_spe=None,
                            vlines=None, vline_styles=None, vline_colors=None, vline_labels=None, vline_widths=None,
                            hlines=None, hline_styles=None, hline_colors=None, hline_labels=None, hline_widths=None,
                            xlog=False, invertX=False, ylog=False, invertY=False, 
                            loc_legend='best', legend_frame=False,
                            font_size=12, usetex=False,
                            fill_between_xs_list=None, 
                            fill_between_yLows_list=None, fill_between_yHighs_list=None,
                            fill_between_COLORs_list=None, fill_between_alphas_list=None,
                            LABEL_position='inSub', LABEL_position_SUBid=0,
                            LABEL_cols=1,
                            FIGSIZE=[6.4, 4.8],
                            TIGHT=False, 
                            N_rows=None, N_cols=None,
                            sharex=True, sharey=True,
                            YLABEL_list=None,
                            YRANGE_list=None,
                            no_xticklabels_list=None,
                            no_yticklabels_list=None, 
                            font_type="serif",
                            xerrs_list=None):
    """
    Errorbar plot for multiple subplots
    """

    if outpath != 'show':
        backend_orig = plt.get_backend()
        plt.switch_backend("agg")

    # font size
    plt.rc('font', size=font_size)
    # tex
    plt.rcParams["text.usetex"] = usetex
    # the font
    plt.rcParams['font.family'] = font_type

    if N_rows is None:
        N_rows = math.ceil(N_plots**0.5)
        N_cols = math.ceil(N_plots/N_rows)
    fig, axs = plt.subplots(N_rows, N_cols, sharex=sharex, sharey=sharey, figsize=FIGSIZE)
    fig.subplots_adjust(hspace=0)
    fig.subplots_adjust(wspace=0)

    if TIGHT:
        # for x,y label
        fig.add_subplot(111, frameon=False)
        # hide tick and tick label of the big axes
        plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
        plt.grid(False)
        # plt.xlabel(XLABEL)
        # plt.ylabel(YLABEL)
        if TITLE is not None:
            plt.title(TITLE)

    i_plot = 0
    handles = []
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

                xvals = xvals_list[i_plot]
                yvals = yvals_list[i_plot]
                if yerrs_list is not None:
                    yerrs = yerrs_list[i_plot]
                else:
                    yerrs = None
                if xerrs_list is not None:
                    xerrs = xerrs_list[i_plot]
                else:
                    xerrs = None

                COLORs = COLORs_list[i_plot]

                if LABELs_list is not None:
                    LABELs = LABELs_list[i_plot]
                else:
                    LABELs = None

                if LINEs_list is not None:
                    LINEs = LINEs_list[i_plot]
                else:
                    LINEs = None
                if LINEWs_list is not None:
                    LINEWs = LINEWs_list[i_plot]
                else:
                    LINEWs = None

                if POINTs_list is not None:
                    POINTs = POINTs_list[i_plot]
                else:
                    POINTs = None
                if POINTSs_list is not None:
                    POINTSs = POINTSs_list[i_plot]
                else:
                    POINTSs = None
                if ERRORSIZEs_list is not None:
                    ERRORSIZEs = ERRORSIZEs_list[i_plot]
                else:
                    ERRORSIZEs = None

                for i, xvl in enumerate(xvals):
                    yvl = yvals[i]
                    if yerrs is not None:
                        if yerrs[i] is not None:
                            yerr = np.array(yerrs[i])
                            yerr = np.vstack([yerr[0], yerr[1]])
                        else:
                            yerr = None
                    else:
                        yerr = None
                    if xerrs is not None:
                        if xerrs[i] is not None:
                            xerr = np.array(xerrs[i])
                            xerr = np.vstack([xerr[0], xerr[1]])
                        else:
                            xerr = None
                    else:
                        xerr = None

                    CR = COLORs[i]

                    if LABELs is not None:
                        LAB = LABELs[i]
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

                    tmp = ax.errorbar(xvl, yvl, xerr=xerr, yerr=yerr, color=CR, label=LAB, linestyle=LN, linewidth=LW, marker=PI, markersize=MS, capsize=ERRORSIZE)
                    if (LABEL_position!='inSub') and (i_plot==0):
                        handles.append(tmp)
                    del tmp

                if (LABEL_position=='inSub') and (LABELs is not None) and (i_plot == LABEL_position_SUBid):
                    ax.legend(frameon=legend_frame, loc=loc_legend)

                if fill_between_xs_list is not None:
                    fill_between_xs = fill_between_xs_list[i_plot]
                    fill_between_yLows = fill_between_yLows_list[i_plot]
                    fill_between_yHighs = fill_between_yHighs_list[i_plot]
                    fill_between_COLORs = fill_between_COLORs_list[i_plot]
                    fill_between_alphas = fill_between_alphas_list[i_plot]
                    for i_fill, fill_between_x in enumerate(fill_between_xs):
                        ax.fill_between(fill_between_x, 
                                    fill_between_yLows[i_fill], fill_between_yHighs[i_fill],
                                    alpha=fill_between_alphas[i_fill],
                                    color=fill_between_COLORs[i_fill])

                if subLABEL_list is not None:
                    LABEL = subLABEL_list[i_plot]
                    ax.text(subLABEL_locX, subLABEL_locY, LABEL, transform=ax.transAxes,
                        bbox=subLABEL_bbox)

                if XRANGE is not None:
                    ax.set_xlim(XRANGE[0], XRANGE[1])
                if YRANGE is not None:
                    ax.set_ylim(YRANGE[0], YRANGE[1])

                if YRANGE_list is not None:
                    ax.set_ylim(YRANGE_list[i_plot][0], YRANGE_list[i_plot][1])

                if YLABEL_list is not None:
                    ax.set_ylabel(YLABEL_list[i_plot])

                if vlines is not None:
                    _vhlines('v', vlines, line_styles=vline_styles, line_colors=vline_colors, line_labels=vline_labels, line_widths=vline_widths, ax=ax)
                if hlines is not None:
                    _vhlines('h', hlines, line_styles=hline_styles, line_colors=hline_colors, line_labels=hline_labels, line_widths=hline_widths, ax=ax)

                if xlog:
                    ax.set_xscale('log')
                    ax.xaxis.set_minor_formatter(NullFormatter())
                if ylog:
                    ax.set_yscale('log')

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
                    ax.set_xticks(xtick_spe[0])
                    ax.set_xticklabels(xtick_spe[1])
                if ytick_spe is not None:
                    ax.set_yticks(ytick_spe[0])
                    ax.set_yticklabels(ytick_spe[1])

                if (no_xticklabels_list is not None) and (no_xticklabels_list[i_plot]):
                    ax.set_xticklabels([])

                if (no_yticklabels_list is not None) and (no_yticklabels_list[i_plot]):
                    ax.set_yticklabels([])

                if invertY:
                    plt.gca().invert_yaxis()
                if invertX:
                    plt.gca().invert_xaxis()

            i_plot +=1

    fig.text(0.5, 0.01, XLABEL, ha='center', va='bottom')
    fig.text(0.01, 0.5, YLABEL, ha='left', va='center', rotation='vertical')

    if TITLE is not None:
        fig.text(0.5, 0.90, TITLE, ha='center')

    if (LABEL_position=='right') and (LABELs is not None):
        fig.legend(handles, LABELs, 
                loc = 'upper right',
                bbox_to_anchor=(0.92, 0.35), fancybox=True, shadow=True)

    if (LABEL_position=='top') and (LABELs is not None):
        fig.legend(handles, LABELs, 
                loc = 'center', ncol=LABEL_cols,
                bbox_to_anchor=(0.5, 0.95), fancybox=True, shadow=True)

    if TIGHT:
        plt.tight_layout()

    if outpath == 'show':
        plt.show()
        plt.close()
    else:
        plt.savefig(outpath, dpi=300)
        plt.close()
        plt.switch_backend(backend_orig)
        print("Errorbar plot saved as", outpath)

def ScatterPlotFunc(outpath,
                xval, yval, POINT=None, POINTS=None, alpha=None,
                cval=None, cmap=None, cmin=None, cmax=None, clog=False,
                bar_loc=None, bar_ori=None, bar_label=None, bar_tick=None,
                XRANGE=None, YRANGE=None,
                XLABEL=None, YLABEL=None, TITLE=None,
                xtick_min_label=True, xtick_spe=None, ytick_min_label=True, ytick_spe=None,
                vlines=None, vline_styles=None, vline_colors=None, vline_labels=None, vline_widths=None,
                hlines=None, hline_styles=None, hline_colors=None, hline_labels=None, hline_widths=None,
                xlog=False, invertX=False, ylog=False, invertY=False, 
                loc_legend='best', legend_frame=False,
                font_size=12, usetex=False,
                FIGSIZE=[6.4, 4.8],
                texPacks=None):
    """
    scatter plot with colourful points
        only support for one set of parameters
        for multi sets of parameters use LinePlotFunc
    """

    # font size
    plt.rc('font', size=font_size)
    # tex
    plt.rcParams["text.usetex"] = usetex
    if texPacks is not None:
        for texPack in texPacks:
            plt.rcParams['text.latex.preamble']=texPack

    if outpath != 'show':
        backend_orig = plt.get_backend()
        plt.switch_backend("agg")

    fig, ax = plt.subplots(figsize=FIGSIZE)

    if clog:
        norm = mpl.colors.LogNorm(vmin=cmin, vmax=cmax)
    else:
        norm = mpl.colors.Normalize(vmin=cmin, vmax=cmax)
    plt.scatter(xval, yval, s=POINTS, c=cval, marker=POINT,
                cmap=cmap, norm=norm, alpha=alpha)

    if cval is not None:
        plt.colorbar(location=bar_loc, orientation=bar_ori, ticks=bar_tick, label=bar_label)

    if XRANGE is not None:
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

    if invertX:
        plt.gca().invert_xaxis()
    if invertY:
        plt.gca().invert_yaxis()

    plt.xlabel(XLABEL)
    plt.ylabel(YLABEL)
    if TITLE is not None:
        plt.title(TITLE)

    plt.tight_layout()

    if outpath=='show':
        plt.show()
        plt.close()
    else:
        plt.savefig(outpath, dpi=300)
        plt.close()
        plt.switch_backend(backend_orig)
        print("Scatter plot saved as", outpath)

def ErrorPlotFunc_2sub_shareX(outpath,
                xvals_u, yvals_u, yerrs_u,
                xvals_d, yvals_d, yerrs_d,
                COLORs_u, COLORs_d,
                LABELs_u=None, LINEs_u=None, LINEWs_u=None, POINTs_u=None, POINTSs_u=None, ERRORSIZEs_u=None,
                LABELs_d=None, LINEs_d=None, LINEWs_d=None, POINTs_d=None, POINTSs_d=None, ERRORSIZEs_d=None,
                XRANGE=None, YRANGE_u=None, YRANGE_d=None,
                XLABEL=None, YLABEL_u=None, YLABEL_d=None, TITLE=None,
                xtick_min_label=True, xtick_spe=None, 
                ytick_min_label_u=True, ytick_spe_u=None,
                ytick_min_label_d=True, ytick_spe_d=None,
                vlines=None, vline_styles=None, vline_colors=None, vline_labels=None, vline_widths=None,
                hlines_u=None, hline_styles_u=None, hline_colors_u=None, hline_labels_u=None, hline_widths_u=None,
                hlines_d=None, hline_styles_d=None, hline_colors_d=None, hline_labels_d=None, hline_widths_d=None,
                xlog=False, invertX=False, 
                ylog_u=False, invertY_u=False, ylog_d=False, invertY_d=False, 
                loc_legend_u='best', legend_frame_u=False, frame_alpha_u=0.8,
                loc_legend_d='best', legend_frame_d=False, frame_alpha_d=0.8,
                fill_between_xs_u=None, 
                fill_between_yLows_u=None, fill_between_yHighs_u=None,
                fill_between_COLORs_u=None, fill_between_alphas_u=None,
                fill_between_xs_d=None, 
                fill_between_yLows_d=None, fill_between_yHighs_d=None,
                fill_between_COLORs_d=None, fill_between_alphas_d=None,
                font_size=12, usetex=False,
                xerrs_u=None, xerrs_d=None, 
                alpha_list_u = None, zorder_list_u = None,
                alpha_list_d = None, zorder_list_d = None,
                FIGSIZE=[6.4, 4.8],
                transparent=False,
                font_size_label=None):
    """
    Errorbar plot for multiple parameters
    """

    # font size
    plt.rc('font', size=font_size)
    if font_size_label is None:
        font_size_label = font_size
    # tex
    plt.rcParams["text.usetex"] = usetex

    if outpath != 'show':
        backend_orig = plt.get_backend()
        plt.switch_backend("agg")

    # two subplots with ratio: 3:1
    fig, axs = plt.subplots(2, 1, figsize=FIGSIZE, gridspec_kw={'height_ratios': [3, 1]})

    # the upper plot
    for i, xvl in enumerate(xvals_u):
        yvl = yvals_u[i]
        if yerrs_u is not None:
            yerr = yerrs_u[i]
            if yerr is not None:
                yerr = np.array(yerr)
                yerr = np.vstack([yerr[0], yerr[1]])
        else:
            yerr = None

        if xerrs_u is not None:
            xerr = xerrs_u[i]
            if xerr is not None:
                xerr = np.array(xerr)
                xerr = np.vstack([xerr[0], xerr[1]])
        else:
            xerr = None

        CR = COLORs_u[i]

        if alpha_list_u is not None:
            alpha = alpha_list_u[i]
        else:
            alpha = None
        if zorder_list_u is not None:
            zorder = zorder_list_u[i]
        else:
            zorder = i + 1

        if LABELs_u is not None:
            LAB = LABELs_u[i]
        else:
            LAB = None

        if LINEs_u is not None:
            LN = LINEs_u[i]
        else:
            LN = '--'
        if LINEWs_u is not None:
            LW = LINEWs_u[i]
        else:
            LW = 1

        if POINTs_u is not None:
            PI = POINTs_u[i]
        else:
            PI = 'o'
        if POINTSs_u is not None:
            MS = POINTSs_u[i]
        else:
            MS = 2

        if ERRORSIZEs_u is not None:
            ERRORSIZE = ERRORSIZEs_u[i]
        else:
            ERRORSIZE = 2

        axs[0].errorbar(xvl, yvl, xerr=xerr, yerr=yerr, 
            color=CR, label=LAB, linestyle=LN, linewidth=LW, marker=PI, markersize=MS, capsize=ERRORSIZE,
            alpha=alpha,
            zorder=zorder)

    if fill_between_xs_u is not None:
        for i_fill, fill_between_x in enumerate(fill_between_xs_u):
            axs[0].fill_between(fill_between_x, 
                        fill_between_yLows_u[i_fill], fill_between_yHighs_u[i_fill],
                        alpha=fill_between_alphas_u[i_fill],
                        color=fill_between_COLORs_u[i_fill])

    if YRANGE_u is not None:
        axs[0].set_ylim(YRANGE_u[0], YRANGE_u[1])

    if ylog_u:
        axs[0].set_yscale('log')

    if vlines is not None:
        _vhlines('v', vlines, 
                line_styles=vline_styles, line_colors=vline_colors, line_labels=vline_labels, line_widths=vline_widths,
                ax=axs[0])

    if hlines_u is not None:
        _vhlines('h', hlines_u, 
                line_styles=hline_styles_u, line_colors=hline_colors_u, line_labels=hline_labels_u, line_widths=hline_widths_u,
                ax=axs[0])

    if LABELs_u is not None:
        axs[0].legend(frameon=legend_frame_u, framealpha=frame_alpha_u,
                      loc=loc_legend_u, fontsize=font_size_label)

    if ytick_min_label_u:
        if ylog_u:
            axs[0].yaxis.set_minor_locator(LogLocator(base=10.0, subs=None, numticks=10))
        else:
            axs[0].yaxis.set_minor_locator(AutoMinorLocator())

    if ytick_spe_u is not None:
        axs[0].set_yticks(ytick_spe_u[0], ytick_spe_u[1])

    if invertY_u:
        axs[0].invert_yaxis()

    axs[0].set_ylabel(YLABEL_u)
    if TITLE is not None:
        axs[0].set_title(TITLE)

    # the lower plot
    for i, xvl in enumerate(xvals_d):
        yvl = yvals_d[i]
        if yerrs_d is not None:
            yerr = yerrs_d[i]
            if yerr is not None:
                yerr = np.array(yerr)
                yerr = np.vstack([yerr[0], yerr[1]])
        else:
            yerr = None

        if xerrs_d is not None:
            xerr = xerrs_d[i]
            if xerr is not None:
                xerr = np.array(xerr)
                xerr = np.vstack([xerr[0], xerr[1]])
        else:
            xerr = None

        CR = COLORs_d[i]

        if alpha_list_d is not None:
            alpha = alpha_list_d[i]
        else:
            alpha = None
        if zorder_list_d is not None:
            zorder = zorder_list_d[i]
        else:
            zorder = i + 1

        if LABELs_d is not None:
            LAB = LABELs_d[i]
        else:
            LAB = None

        if LINEs_d is not None:
            LN = LINEs_d[i]
        else:
            LN = '--'
        if LINEWs_d is not None:
            LW = LINEWs_d[i]
        else:
            LW = 1

        if POINTs_d is not None:
            PI = POINTs_d[i]
        else:
            PI = 'o'
        if POINTSs_d is not None:
            MS = POINTSs_d[i]
        else:
            MS = 2

        if ERRORSIZEs_d is not None:
            ERRORSIZE = ERRORSIZEs_d[i]
        else:
            ERRORSIZE = 2

        axs[1].errorbar(xvl, yvl, xerr=xerr, yerr=yerr, 
            color=CR, label=LAB, linestyle=LN, linewidth=LW, marker=PI, markersize=MS, capsize=ERRORSIZE,
            alpha=alpha,
            zorder=zorder)

    if fill_between_xs_d is not None:
        for i_fill, fill_between_x in enumerate(fill_between_xs_d):
            axs[1].fill_between(fill_between_x, 
                        fill_between_yLows_d[i_fill], fill_between_yHighs_d[i_fill],
                        alpha=fill_between_alphas_d[i_fill],
                        color=fill_between_COLORs_d[i_fill])

    if YRANGE_d is not None:
        axs[1].set_ylim(YRANGE_d[0], YRANGE_d[1])

    if ylog_d:
        axs[1].set_yscale('log')

    if vlines is not None:
        _vhlines('v', vlines, 
                 line_styles=vline_styles, line_colors=vline_colors, line_labels=vline_labels, line_widths=vline_widths,
                 ax=axs[1])

    if hlines_d is not None:
        _vhlines('h', hlines_d, 
                line_styles=hline_styles_d, line_colors=hline_colors_d, line_labels=hline_labels_d, line_widths=hline_widths_d,
                ax=axs[1])

    if LABELs_d is not None:
        axs[1].legend(frameon=legend_frame_d, framealpha=frame_alpha_d,
                      loc=loc_legend_d, fontsize=font_size_label)

    if ytick_min_label_d:
        if ylog_d:
            axs[1].yaxis.set_minor_locator(LogLocator(base=10.0, subs=None, numticks=10))
        else:
            axs[1].yaxis.set_minor_locator(AutoMinorLocator())

    if ytick_spe_d is not None:
        axs[1].set_yticks(ytick_spe_d[0], ytick_spe_d[1])

    if invertY_d:
        axs[1].invert_yaxis()

    axs[1].set_ylabel(YLABEL_d)

    # share the x
    axs[0].get_shared_x_axes().join(axs[0], axs[1])
    # Hide top x-tick labels 
    axs[0].tick_params(labelbottom=False)
    # x axis info
    if XRANGE is not None:
        plt.xlim(XRANGE[0], XRANGE[1])
    if xlog:
        plt.xscale('log')
    if xtick_min_label:
        if xlog:
            axs[0].xaxis.set_minor_locator(LogLocator(base=10.0, subs=None, numticks=10))
        else:
            axs[0].xaxis.set_minor_locator(AutoMinorLocator())
    if xtick_spe is not None:
        plt.xticks(xtick_spe[0], xtick_spe[1])
    if invertX:
        plt.gca().invert_xaxis()

    axs[1].set_xlabel(XLABEL)

    plt.tight_layout()

    if outpath=='show':
        plt.show()
        plt.close()
    else:
        plt.savefig(outpath, dpi=300, transparent=transparent)
        plt.close()
        plt.switch_backend(backend_orig)
        print("Errorbar plot saved in", outpath)

