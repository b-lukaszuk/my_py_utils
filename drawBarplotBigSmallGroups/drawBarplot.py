import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns


def draw_barplot_means_sds(
    tab_with_data: pd.DataFrame,
    tab_with_signif_markers: pd.DataFrame,
    col_with_digits: str,
    col_big_group: str,
    col_small_group: str,
    order_big_group: [str],
    labels_big_group: [str],
    order_small_group: [str],
    labels_small_group: [str],
    colors_small_group: [(float)],
    main_title: str,
    y_axis_title: str,
    x_axis_title: str,
    draw_points: bool = False,
    use_sem: bool = False,
) -> mpl.axes:
    """
    draws a barplot (with signif_markers) grouped by big_group and small_group

    Input:
    ---
    tab_with_data - df with oryginal data, columns: [val1, val2, gr1, gr2]
    tab_with_signif_markers - col_names: [bg1_sg1, bg1_sg2, bg2_sg1, bg2_sg2],
                              row_names=[val1, val2]
    col_with_digits - name of the column with digits for which we draw barplot
    col_big_group - name of the column with 'big grouping' (clusters of bars)
    col_small_group - name of the column with 'smal grouping'
                                      (bars within a cluster)
    order_big_group - order of big groups (left to right) on the graph
    labels_big_group - labels of big_gr displayed on the graph (x-axis ticks)
    order_small_group - order of small groups (left to right) in the cluster
    labels_small_group - labels of small groups (displayed on legend)
    colors_small_group - colors of small_gr (bars withing a cluster and legend)
    main_title - title of the graph
    y_axis_title - title on the y-axis (over y-axis, on the left)
    x_axis_title - title on the (under) x-axis
    draw_points - should overlay points (sns.swarmplot) on bars
    use_sem - should use standard error of the mean as whiskers instead of sd

    Output:
    ---
    a graph (barplot) - mpl.axes object
    bg - big_group (1, 2, 3...) - localization of bar groups (0, 1, 2, ..., n)
    sg - small_group (1, 2, 3...) - localization of bars within a group
    graph outlook
    bg1_sg1, bg1_sg2, bg1_sg3,...    bg2_sg1, bg2_sg2, bg2_sg3,...
    """

    grouped_data: pd.DataFrame = tab_with_data[
        [col_with_digits, col_big_group, col_small_group]
    ].groupby([col_big_group, col_small_group])

    means: pd.DataFrame = grouped_data.mean().reset_index()
    stds: pd.DataFrame = grouped_data.std().reset_index()
    extra_space_above_cap = 1.17  # should be > 1

    if use_sem:
        stds = grouped_data.sem().reset_index()
    if draw_points:
        extra_space_above_cap = 1.8
    if draw_points and use_sem:
        extra_space_above_cap = 2.8

    maks_val: float = (
        means[col_with_digits].max() + stds[col_with_digits].max()
    ) * extra_space_above_cap
    signif_makrers_heights: pd.DataFrame = means.copy()
    signif_makrers_heights[col_with_digits] = (
        signif_makrers_heights[col_with_digits] + stds[col_with_digits]
    ) + (
        maks_val * 0.1
    )  # + (maks_val * 0.04) additonal space between maker and whisker cap

    plt.grid(
        visible=True,  # was: b=True
        linestyle="dashed",
        which="major",
        alpha=0.6,
        axis="y",
        color="grey",
        dashes=(5, 2),
        zorder=0,
    )

    g: mpl.axes = sns.barplot(
        x=tab_with_data.loc[:, col_big_group],
        y=tab_with_data.loc[:, col_with_digits],
        hue=tab_with_data.loc[:, col_small_group],
        palette=colors_small_group,
        order=order_big_group,
        hue_order=order_small_group,
        capsize=0.65,
        err_kws={"linewidth": 3},
        edgecolor="black",
        linewidth=3,
        errorbar="se" if use_sem else "sd",
        zorder=2,
    )

    if draw_points:
        sns.swarmplot(
            x=tab_with_data.loc[:, col_big_group],
            y=tab_with_data.loc[:, col_with_digits],
            hue=tab_with_data.loc[:, col_small_group],
            palette=colors_small_group,
            order=order_big_group,
            dodge=True,
            hue_order=order_small_group,
            size=15,
            edgecolor="black",
            linewidth=2,
            alpha=0.5,
            zorder=3,
        )

    ticks_big: [int] = list(range(len(order_big_group)))
    bar_width: float = g.patches[0].get_width()
    bars_per_big_group: int = len(order_small_group)
    half_way: float = bar_width * bars_per_big_group / 2
    ticks_small: [float] = [
        j
        for tick_big in ticks_big
        for j in np.linspace(
            start=tick_big - half_way + (bar_width / 2),
            stop=tick_big + half_way - (bar_width / 2),
            num=bars_per_big_group,
        )
    ]

    # only upper whisker of sd is visible
    for bar in g.patches:
        bar.set_zorder(3)

    axes = plt.gca()
    axes.set_ylim([0, maks_val * 1.1])  # 1.1 additional space,
    # e.g so that legend would not overlap with signif_markers

    handles1: [mpatches.Patch] = []
    for i in range(len(order_small_group)):
        handles1.append(
            mpatches.Patch(
                edgecolor="black",
                linewidth=2,
                facecolor=colors_small_group[i],
                label=labels_small_group[i],
            )
        )

    plt.legend(handles=handles1, loc="best")

    counter: int = 0
    for big_group in order_big_group:
        for small_group in order_small_group:
            plt.text(
                x=ticks_small[counter],
                y=signif_makrers_heights[
                    np.logical_and(
                        signif_makrers_heights[col_small_group] == small_group,
                        signif_makrers_heights[col_big_group] == big_group,
                    )
                ][col_with_digits].iloc[0],
                s=tab_with_signif_markers.loc[
                    col_with_digits, big_group + "_" + small_group
                ],
                horizontalalignment="center",
                fontdict={"fontsize": 30},
                zorder=4,
            )
            counter += 1

    plt.title(label=main_title)
    plt.xlabel(xlabel=x_axis_title)
    plt.ylabel(ylabel=y_axis_title)
    plt.xticks(ticks=ticks_big, labels=labels_big_group)


def draw_simple_barplot_means_sds(
    tab_with_data: pd.DataFrame,
    tab_with_signif_markers: pd.DataFrame,
    col_with_digits: str,
    col_group: str,
    order_group: [str],
    labels_group: [str],
    colors_group: [(float)],
    main_title: str,
    y_axis_title: str,
    x_axis_title: str,
    draw_points: bool = False,
    use_sem: bool = False,
) -> mpl.axes:
    """
    draws a barplot (with signif_markers)

    Input:
    ---
    tab_with_data - df with oryginal data, columns: [val1, val2, gr1, gr2, ...]
    tab_with_signif_markers - col_names: [gr1, gr2,...], row_names=[val1, val2]
    col_with_digits - name of the column with digits for which we draw barplot
    col_group - name of the column with group labels
    order_group - order of groups (left to right) on the graph
    labels_group - labels of big_gr displayed on the graph (x-axis ticks)
    colors_group - colors of groups
    main_title - title of the graph
    y_axis_title - title on the y-axis (over y-axis, on the left)
    x_axis_title - title on the (under) x-axis
    draw_points - should overlay points (sns.swarmplot) on bars
    use_sem - should use standard error of the mean as whiskers instead of sd

    Output:
    ---
    a graph (barplot) - mpl.axes object
    """

    grouped_data: pd.DataFrame = tab_with_data[
        [col_with_digits, col_group]].groupby([col_group])

    means: pd.DataFrame = grouped_data.mean().reset_index()
    stds: pd.DataFrame = grouped_data.std().reset_index()
    extra_space_above_cap = 1.17  # should be > 1

    if use_sem:
        stds = grouped_data.sem().reset_index()
    if draw_points:
        extra_space_above_cap = 1.8
    if draw_points and use_sem:
        extra_space_above_cap = 2.8

    maks_val: float = (
        means[col_with_digits].max() + stds[col_with_digits].max()
    ) * extra_space_above_cap
    signif_makrers_heights: pd.DataFrame = means.copy()
    signif_makrers_heights[col_with_digits] = (
        signif_makrers_heights[col_with_digits] + stds[col_with_digits]
    ) + (
        maks_val * 0.1
    )  # + (maks_val * 0.04) additonal space between maker and whisker cap

    plt.grid(
        visible=True,  # was: b=True
        linestyle="dashed",
        which="major",
        alpha=0.6,
        axis="y",
        color="grey",
        dashes=(5, 2),
        zorder=0,
    )

    g: mpl.axes = sns.barplot(
        x=tab_with_data.loc[:, col_group],
        y=tab_with_data.loc[:, col_with_digits],
        hue=tab_with_data.loc[:, col_group],
        palette=colors_group,
        legend=False,
        order=order_group,
        hue_order=order_group,
        capsize=0.65,
        err_kws={"linewidth": 3},
        edgecolor="black",
        linewidth=3,
        errorbar="se" if use_sem else "sd",
        zorder=2,
    )

    if draw_points:
        sns.swarmplot(
            x=tab_with_data.loc[:, col_group],
            y=tab_with_data.loc[:, col_with_digits],
            hue=tab_with_data.loc[:, col_group],
            palette=colors_group,
            legend=False,
            order=order_group,
            dodge=False,
            hue_order=order_group,
            size=15,
            edgecolor="black",
            linewidth=2,
            alpha=0.5,
            zorder=3,
        )

    ticks_big: [int] = list(range(len(order_group)))

    # only upper whisker of sd is visible
    for bar in g.patches:
        bar.set_zorder(3)

    axes = plt.gca()
    axes.set_ylim([0, maks_val * 1.1])  # 1.1 additional space,
    # e.g so that legend would not overlap with signif_markers

    handles1: [mpatches.Patch] = []
    for i in range(len(order_group)):
        handles1.append(
            mpatches.Patch(
                edgecolor="black",
                linewidth=2,
                facecolor=colors_group[i],
                label=labels_group[i],
            )
        )

    plt.legend(handles=handles1, loc="best")

    counter: int = 0
    for big_group in order_group:
        plt.text(
            x=ticks_big[counter],
            y=signif_makrers_heights.loc[
                [gr == big_group for gr in signif_makrers_heights[col_group]],
                col_with_digits].iloc[0],
            s=tab_with_signif_markers.loc[col_with_digits, big_group],
            horizontalalignment="center",
            fontdict={"fontsize": 30},
            zorder=4,
        )
        counter += 1

    plt.title(label=main_title)
    plt.xlabel(xlabel=x_axis_title)
    plt.ylabel(ylabel=y_axis_title)
    plt.xticks(ticks=ticks_big, labels=labels_group)


def draw_boxplot(
    tab_with_data: pd.DataFrame,
    tab_with_signif_markers: pd.DataFrame,
    col_with_digits: str,
    col_big_group: str,
    col_small_group: str,
    order_big_group: [str],
    labels_big_group: [str],
    order_small_group: [str],
    labels_small_group: [str],
    colors_small_group: [(float)],
    main_title: str,
    y_axis_title: str,
    x_axis_title: str,
) -> mpl.axes:
    """
    draws a barplot (with signif_markers) grouped by big_group and small_group

    Input:
    ---
    tab_with_data - df with oryginal data, columns: [val1, val2, gr1, gr2]
    tab_with_signif_markers - col_names: [bg1_sg1, bg1_sg2, bg2_sg1, bg2_sg2],
                              row_names=[val1, val2]
    col_with_digits - name of the column with digits for which we draw barplot
    col_big_group - name of the column with 'big grouping' (clusters of bars)
    col_small_group - name of the column with 'smal grouping'
                                      (bars within a cluster)
    order_big_group - order of big groups (left to right) on the graph
    labels_big_group - labels of big_gr displayed on the graph (x-axis ticks)
    order_small_group - order of small groups (left to right) in the cluster
    labels_small_group - labels of small groups (displayed on legend)
    colors_small_group - colors of small_gr (bars withing a cluster and legend)
    main_title - title of the graph
    y_axis_title - title on the y-axis (over y-axis, on the left)
    x_axis_title - title on the (under) x-axis

    Output:
    ---
    a graph (barplot) - mpl.axes object
    bg - big_group (1, 2, 3...) - localization of bar groups (0, 1, 2, ..., n)
    sg - small_group (1, 2, 3...) - localization of bars within a group
    graph outlook
    bg1_sg1, bg1_sg2, bg1_sg3,...    bg2_sg1, bg2_sg2, bg2_sg3,...
    """

    grouped_data: pd.DataFrame = tab_with_data[
        [col_with_digits, col_big_group, col_small_group]
    ].groupby([col_big_group, col_small_group])

    maxes: pd.DataFrame = grouped_data.max().reset_index()

    maks_val: float = (
        maxes[col_with_digits].max() * 1.17
    )  # 1.17 adds additional free space above whisker cap
    signif_makrers_heights: pd.DataFrame = maxes.copy()
    # + (maks_val * 0.04) additonal space between maker and whisker cap
    signif_makrers_heights[col_with_digits] = (
        signif_makrers_heights[col_with_digits]
    ) + (maks_val * 0.1)

    plt.grid(
        visible=True,  # was: b=True
        linestyle="dashed",
        which="major",
        alpha=0.6,
        axis="y",
        color="grey",
        dashes=(5, 2),
        zorder=0,
    )

    sns.boxplot(
        x=tab_with_data.loc[:, col_big_group],
        y=tab_with_data.loc[:, col_with_digits],
        hue=tab_with_data.loc[:, col_small_group],
        palette=colors_small_group,
        order=order_big_group,
        hue_order=order_small_group,
        linewidth=3,
    )

    ticks_big: [int] = list(range(len(order_big_group)))
    box_width: float = 0.4  # default box width in seaborn
    boxes_per_big_group: int = len(order_small_group)
    half_way: float = box_width * boxes_per_big_group / 2
    ticks_small: [float] = [
        j
        for tick_big in ticks_big
        for j in np.linspace(
            start=tick_big - half_way + (box_width / 2),
            stop=tick_big + half_way - (box_width / 2),
            num=boxes_per_big_group,
        )
    ]

    axes = plt.gca()
    axes.set_ylim([0, maks_val * 1.1])  # 1.1 additional space,
    # e.g so that legend would not overlap with signif_markers

    handles1: [mpatches.Patch] = []
    for i in range(len(order_small_group)):
        handles1.append(
            mpatches.Patch(
                edgecolor="black",
                linewidth=2,
                facecolor=colors_small_group[i],
                label=labels_small_group[i],
            )
        )

    plt.legend(handles=handles1, loc="best")

    counter: int = 0
    for big_group in order_big_group:
        for small_group in order_small_group:
            plt.text(
                x=ticks_small[counter],
                y=signif_makrers_heights[
                    np.logical_and(
                        signif_makrers_heights[col_small_group] == small_group,
                        signif_makrers_heights[col_big_group] == big_group,
                    )
                ][col_with_digits].iloc[0],
                s=tab_with_signif_markers.loc[
                    col_with_digits, big_group + "_" + small_group
                ],
                horizontalalignment="center",
                fontdict={"fontsize": 26},
                zorder=4,
            )
            counter += 1

    plt.title(label=main_title)
    plt.xlabel(xlabel=x_axis_title)
    plt.ylabel(ylabel=y_axis_title)
    plt.xticks(ticks=ticks_big, labels=labels_big_group)


def draw_simple_boxplot(
    tab_with_data: pd.DataFrame,
    tab_with_signif_markers: pd.DataFrame,
    col_with_digits: str,
    col_group: str,
    order_group: [str],
    labels_group: [str],
    colors_group: [(float)],
    main_title: str,
    y_axis_title: str,
    x_axis_title: str,
) -> mpl.axes:
    """
    draws a barplot (with signif_markers)

    Input:
    ---
    tab_with_data - df with oryginal data, columns: [val1, val2, gr1, gr2, ...]
    tab_with_signif_markers - col_names: [gr1, gr2,...], row_names=[val1, val2]
    col_with_digits - name of the column with digits for which we draw barplot
    col_group - name of the column with group labels
    order_group - order of groups (left to right) on the graph
    labels_group - labels of big_gr displayed on the graph (x-axis ticks)
    colors_group - colors of groups
    main_title - title of the graph
    y_axis_title - title on the y-axis (over y-axis, on the left)
    x_axis_title - title on the (under) x-axis

    Output:
    ---
    a graph (barplot) - mpl.axes object
    """

    grouped_data: pd.DataFrame = tab_with_data[[col_with_digits, col_group]].groupby(
        [col_group]
    )

    maxes: pd.DataFrame = grouped_data.max().reset_index()

    maks_val: float = (
        maxes[col_with_digits].max() * 1.17
    )  # 1.17 adds additional free space above whisker cap
    signif_makrers_heights: pd.DataFrame = maxes.copy()
    # + (maks_val * 0.04) additonal space between maker and whisker cap
    signif_makrers_heights[col_with_digits] = (
        signif_makrers_heights[col_with_digits]
    ) + (maks_val * 0.1)

    plt.grid(
        visible=True,  # was: b=True
        linestyle="dashed",
        which="major",
        alpha=0.6,
        axis="y",
        color="grey",
        dashes=(5, 2),
        zorder=0,
    )

    sns.boxplot(
        x=tab_with_data.loc[:, col_group],
        y=tab_with_data.loc[:, col_with_digits],
        hue=tab_with_data.loc[:, col_group],
        palette=colors_group,
        legend=False,
        order=order_group,
        hue_order=order_group,
        linewidth=3,
    )

    ticks_big: [int] = list(range(len(order_group)))

    axes = plt.gca()
    axes.set_ylim([0, maks_val * 1.1])  # 1.1 additional space,
    # e.g so that legend would not overlap with signif_markers

    handles1: [mpatches.Patch] = []
    for i in range(len(order_group)):
        handles1.append(
            mpatches.Patch(
                edgecolor="black",
                linewidth=2,
                facecolor=colors_group[i],
                label=labels_group[i],
            )
        )

    plt.legend(handles=handles1, loc="best")

    counter: int = 0
    for big_group in order_group:
        plt.text(
            x=ticks_big[counter],
            y=signif_makrers_heights.loc[
                [gr == big_group for gr in signif_makrers_heights[col_group]],
                col_with_digits,
            ].iloc[0],
            s=tab_with_signif_markers.loc[col_with_digits, big_group],
            horizontalalignment="center",
            fontdict={"fontsize": 26},
            zorder=4,
        )
        counter += 1

    plt.title(label=main_title)
    plt.xlabel(xlabel=x_axis_title)
    plt.ylabel(ylabel=y_axis_title)
    plt.xticks(ticks=ticks_big, labels=labels_group)
