# Usage

<pre>
# optional
# plt.rcParams["figure.facecolor"] = "white"
# plt.rcParams["axes.facecolor"] = "white"

df = pd.read_csv("./mock_data/mock_data.csv", index_col=0)

# optional
# sns.set_context(context="paper")
# plt.figure(figsize=(13, 8))
draw_stackPlot(
    tab_with_data=df,
    groups_names=["gr1", "gr2"],
    molecules_names=["molecule1", "molecule2", "molecule3"],
    order_groups=["gr1", "gr2"],
    labels_groups=["Gr1", "Gr2"],
    order_molecules=["molecule1", "molecule2", "molecule3"],
    labels_molecules=["Molecule1", "Molecule2", "Molecule3"],
    colors_molecules=[(1, 0, 0), (0, 1, 0), (0, 0, 1)],
    main_title="main_title",
    y_axis_title="amount of molecules",
    x_axis_title="groups",
    percentage=False,
)

# optional
# plt.show()
# plt.clf()
</pre>
