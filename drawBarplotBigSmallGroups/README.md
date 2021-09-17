# Usage

<pre>
# optional
# plt.rcParams["figure.facecolor"] = "white"
# plt.rcParams["axes.facecolor"] = "white"
# sns.set_context(context="paper")

df = pd.read_csv("./mock_data/mock_data.csv")
signif_markers = pd.read_csv("./mock_data/mock_markers.csv", index_col=0)
signif_markers = signif_markers.fillna(value="")

# optional
# plt.figure(figsize=(13, 8))

draw_barplot_means_sds(
    tab_with_data=df,
    tab_with_signif_markers=signif_markers,
    col_with_digits="molecule1",
    col_big_group="bg",
    col_small_group="sg",
    order_big_group=["lean", "obese"],
    labels_big_group=["Lean", "Obese"],
    order_small_group=["m", "f"],
    labels_small_group=["M", "F"],
    colors_small_group=[(1, 0, 0), (0, 0, 1)],
    main_title="main title",
    y_axis_title="amount of a molecule1",
    x_axis_title="different groups",
)

# optional
# plt.show()
# plt.clf()
</pre>
