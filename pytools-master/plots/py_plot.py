#!/usr/bin/python

import itertools
import random
import statsmodels.api as sm
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

from matplotlib.ticker import MultipleLocator, FormatStrFormatter


clr_darkblue="#3366cc"
clr_darkred="#dc3912"
clr_darkyellow="#ff9900"
clr_darkgreen="#109618"
clr_darkpurple="#990099"
clr_darkcyan="#0099c6"
clr_black="#000000"
clr_darkorange="#ff6000"

# ================    ===============================
# character           description
# ================    ===============================
# ``'-'``             solid line style
# ``'--'``            dashed line style
# ``'-.'``            dash-dot line style
# ``':'``             dotted line style
# ``'.'``             point marker
# ``','``             pixel marker
# ``'o'``             circle marker
# ``'v'``             triangle_down marker
# ``'^'``             triangle_up marker
# ``'<'``             triangle_left marker
# ``'>'``             triangle_right marker
# ``'1'``             tri_down marker
# ``'2'``             tri_up marker
# ``'3'``             tri_left marker
# ``'4'``             tri_right marker
# ``'s'``             square marker
# ``'p'``             pentagon marker
# ``'*'``             star marker
# ``'h'``             hexagon1 marker
# ``'H'``             hexagon2 marker
# ``'+'``             plus marker
# ``'x'``             x marker
# ``'D'``             diamond marker
# ``'d'``             thin_diamond marker
# ``'|'``             vline marker
# ``'_'``             hline marker
# ================    ===============================


pyplot_markers = [".",",","o","v","^","<",">","1","2","3","4","s",
	"p","*","h","H","+","x","D","d","|","_"]

def ppnext_marker(i):
    return pyplot_markers[i % len(pyplot_markers)]

pyplot_colors = ["b", "g", "r", "c", "m", "y", "k"]

def ppnext_color(i):
    return pyplot_colors[i % len(pyplot_colors)]

pyplot_linestyles = ["-", "--", "-.", ":"]

def ppnext_linestyle(i):
    return pyplot_linestyles[i % len(pyplot_linestyles)]

linepoints_styles = [xx+"-"+yy for xx,yy in itertools.product(pyplot_colors, pyplot_markers)]
random.seed(1234)
random.shuffle(linepoints_styles)


# Fonts ===========================================
# To apply use: matplotlib.rc('font', **font_name)

ppfont_mono = {'family' : 'monospace',
               'weight' : 'bold',
               'size'   : 16}

def make_font(family="monospace", weight="normal", size=16):
    return    {'family' : family,
               'weight' : weight,
               'size'   : size}

# =================================================

def ppset_xlims(ax, xl, xlimprcnt, val_lists):

    if xl:
        ax.set_xlim(xl[0], xl[1])
    elif xlimprcnt:
        xlims = suggest_plots_lims(val_lists, xlimprcnt[0], xlimprcnt[1])
        ax.set_xlim(xlims[0], xlims[1])

def ppset_ylims(ax, yl, ylimprcnt, val_lists):

    if yl:
        ax.set_ylim(yl[0], yl[1])
    elif ylimprcnt:
        ylims = suggest_plots_lims(val_lists, ylimprcnt[0], ylimprcnt[1])
        ax.set_ylim(ylims[0], ylims[1])


def ppset_default_ticks(plot):
    ax = plot.gca()


    ax.xaxis.set_minor_locator(MultipleLocator(4))

    # if ax.get_yscale != "log":
    #     ax.yaxis.set_minor_locator(MultipleLocator(4))


    plot.tick_params(which='minor', length=3, color="k")

    plot.tick_params(which='major', length=6, color="k", width=2)



def create_ecdf_for_plot(samples, num_bins=0):

	ecdf = sm.distributions.ECDF(samples)
	if num_bins == 0:
		num_bins = max(samples) - min(samples)
		num_bins = max(200, num_bins)
		num_bins = min(5000, num_bins)
	x = np.linspace(min(samples), max(samples), num=num_bins)
	y = ecdf(x)
	return x, y




# def suggest_ylims4list_of_lists(data_list, top_cut_prcnt, bottom_cut_prcnt):
#     assert False, "suggest_ylims4list_of_lists is deprecated use suggest_plots_lims"


def suggest_plots_lims(data_lists, bottom_cut_prcnt, top_cut_prcnt):
    """ When plotting a lot of plots automatically, some plots come out bad, because a
    single point can change your Y scale such that you cannot see the rest of the points
    well. This function cuts top and bottom long tails to keep majority of points visible

    Arguments:
        data_lists list of list with points
        top_bottom percentiles: 0-100
    """

    assert top_cut_prcnt > bottom_cut_prcnt

    all_points = [x for sublist in data_lists for x in sublist]

    # max_points = [max(sub_list) for sub_list in data_lists]
    # min_points = [min(sub_list) for sub_list in data_lists]
    ymax = np.percentile(all_points, top_cut_prcnt)
    if bottom_cut_prcnt == 0:
        ymin = min(all_points)
    else:
        ymin = np.percentile(all_points, bottom_cut_prcnt)
    return ymin, ymax


# def plot_point_list(val_lists, ax=None, fig=None, show=True, figsize=(10,7),
#     xl=None, yl=None, xlimprcnt=None, ylimprcnt=None # tuples, hard limits or percentiles))
#     ):

#     if not ax:
#         fig, ax = plt.subplots(figsize=figsize)



def plot_hist_list(val_lists, ax=None, fig=None, show=True, figsize=(10,7),
    xl=None, yl=None, xlimprcnt=None, ylimprcnt=None # tuples, hard limits or percentiles)
    ):
    # Note: ax = plt.gca()

    if not ax:
        fig, ax = plt.subplots(figsize=figsize)

    for hist in val_lists:

        ax.plot(np.arange(len(hist)), hist)



    ppset_xlims(ax, xl, xlimprcnt, val_lists)
    ppset_ylims(ax, yl, ylimprcnt, val_lists)

    ax.grid()
    if show:
        fig.show()

    return fig, ax




# def ppset_default_ticks(ax_axis, plot, interval=4, length=4, color='k'):
#     minorLocator = MultipleLocator(interval)
#     ax_axis.set_minor_locator(minorLocator)

#     if plot:
#         plot.tick_params(which='minor', length=length, color=color)


def plot_cdf_list(val_lists, ax=None, fig=None, show=True, figsize=(10,7),
    xl=None, yl=None, xlimprcnt=None, ylimprcnt=None # tuples, hard limits or percentiles
    ):
    # Note: ax = plt.gca()



    if not ax:
        fig, ax = plt.subplots(figsize=figsize)

    for values in val_lists:

        if not len(values):
            continue
        x, y = create_ecdf_for_plot(
            values,
            # min(len(values), 10000)
            1000000
            )
        ax.plot(x,y)


    ppset_xlims(ax, xl, xlimprcnt, val_lists)
    ppset_ylims(ax, yl, ylimprcnt, val_lists)




    ax.grid()
    if show:
        fig.show()

    return fig, ax