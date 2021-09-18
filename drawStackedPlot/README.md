# Usage

<pre>
# optional
# plt.rcParams["figure.facecolor"] = "white"
# plt.rcParams["axes.facecolor"] = "white"

df = pd.read_csv("./mock_data/mock_data.csv")

# optional
# sns.set_context(context="paper")
# plt.figure(figsize=(13, 8))
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

# optional
# plt.show()
# plt.clf()
</pre>
