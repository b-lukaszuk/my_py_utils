import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


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


def draw_stackPlot(
    tab_with_data: pd.DataFrame,
    groups_names: [str],
    molecules_names: [str],
    order_groups: [str],
    labels_groups: [str],
    order_molecules: [str],
    labels_molecules: [str],
    colors_molecules: [(float)],
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
    labels_groups - labels displayed under the bars (labels for order_groups)
    order_molecules - order of molecules, i.e. of a bar parts (bottom to top)
    labels_molecules - labels for order_molecules displayed in the legend
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

    tab_data: pd.DataFrame = tab_with_data.copy()
    tab_data = tab_data.loc[molecules_names, groups_names]

    if percentage:
        tab_data = dfToColFract(tab_data, True)

    tab_data = tab_data.loc[order_molecules, order_groups]

    maxVal: float = tab_data.sum(axis=0).max()

    plt.grid(
        b=True,
        linestyle="dashed",
        which="major",
        alpha=0.6,
        axis="y",
        color="grey",
        dashes=(5, 2),
        zorder=0,
    )

    x_pos: [int] = list(range(len(groups_names)))
    bar_width: float = 0.5

    bottoms: [float] = [0] * len(groups_names)

    for i in range(len(order_molecules)):
        heights = list(tab_data.loc[order_molecules[i], :])

        plt.bar(
            x=x_pos,
            height=heights,
            bottom=bottoms,
            color=colors_molecules[i],
            edgecolor="black",
            width=bar_width,
            zorder=2,
        )

        bottoms = list(map(lambda x, y: x + y, bottoms, heights))

    axes = plt.gca()
    axes.set_ylim([0, maxVal * 1.2])
    axes.set_xlim([0 - bar_width, max(x_pos) + bar_width])

    handles1: [mpatches.Patch] = []
    for i in range(len(order_molecules)):
        handles1.append(
            mpatches.Patch(
                edgecolor="black",
                linewidth=2,
                facecolor=colors_molecules[i],
                label=labels_molecules[i],
            )
        )

    plt.legend(handles=handles1, loc="best")

    plt.title(label=main_title)
    plt.xlabel(xlabel=x_axis_title)
    plt.ylabel(ylabel=y_axis_title)
    plt.xticks(ticks=x_pos, labels=labels_groups)

    # return 0
