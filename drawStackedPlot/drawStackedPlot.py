import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns


def draw_stackPlot(
    tab_with_data: pd.DataFrame,
    groups_names: [str],
    molecules_names: [str],
    order_groups: [str],
    labels_groups: [str],
    order_molecules: [str],
    labels_molecules: [str],
    colors_molecules: [(int)],
    main_title: str,
    y_axis_title: str,
    x_axis_title: str,
    percentage: bool,
) -> mpl.axes:

    """
    draws a stackbarplot (bars in absolute or percentage quota, one on another)

    Input:
    ---
    tab_with_data - cols: [gr1vals, gr2vals,...], indxs: [submol1, submol2,...]
    groups_names - names of columns (they will be bars on graph)
    molecules_names - names of molecules (indexes) they will compose bars
    order_groups - order of groups (left to right, order of bars on the graph)
    labels_groups - labels displayed under the bars
    order_molecules - order of molecules, i.e. of a bar parts (bottom to top)
    labels_molecules - labels of molecules in the legend
    order_small_group - order of small groups (left to right) in the cluster
    colors_molecules: - colors of bar parts representing given molecules
    main_title - title of the graph
    y_axis_title - title on the y-axis (over y-axis, on the left)
    x_axis_title - title on the (under) x-axis
    percentage - should y axis represent absolute values or pct (upto 100%)

    Output:
    ---
    a graph (stacked barplot or stacked percentage plot) - mpl.axes object
    """

    x_pos: [int] = list(range(len(groups_names)))
    bar_width: float = 0.5

    bottoms: [float] = [0] * len(groups_names)

    for i in range(len(molecules_names)):
        heights = list(tab_with_data.loc[molecules_names[i], :])

        plt.bar(
            x=x_pos,
            height=heights,
            bottom=bottoms,
            color=colors_molecules[i],
            edgecolor="black",
            width=bar_width,
        )

        bottoms = list(map(lambda x, y: x + y, bottoms, heights))

    # return 0
    # plt.title(label=main_title)
    # plt.xlabel(xlabel=x_axis_title)
    # plt.ylabel(ylabel=y_axis_title)
    # plt.xticks(ticks=ticks_big, labels=labels_big_group)


def dfToColFract(df: pd.DataFrame, percentage: bool = True):

    """
    transforms all the numbers in a table to
    fractions of colSums (or percentages)

    Input:
    ---
    df - table to be transformed
    percentage - should y axis represent absolute values or pct (upto 100%)

    Output:
    ---
    new transformed table, each result is val1/colSum1 (optionally: *100)
    """

    colSums: pd.Series = df.sum(axis=0)
    fractions: pd.DataFrame = df / colSums
    if percentage:
        return fractions * 100
    else:
        return fractions
