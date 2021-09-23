Stacked Plot but with 'big' and 'small' groups

# Usage

<pre>
# optional
# plt.rcParams["figure.facecolor"] = "white"
# plt.rcParams["axes.facecolor"] = "white"

df = pd.read_csv("./mock_data/mock_data.csv")

# optional
# sns.set_context(context="paper")
# plt.figure(figsize=(13, 8))
draw_groupedStackPlot(tab_with_data=df,
                      col_big_group="bg",
                      col_small_group="sg",
                      cols_digits=["molecule1", "molecule2", "molecule3"],
                      order_cols_digits=["molecule3", "molecule2", "molecule1"],
                      labels_digits=["Mol3", "Mol2", "Mol1"],
                      colors_digits=[(1, 0, 0), (0, 0, 1), (0.7, 0.7, 0.7)],
                      percentage=False,
                      main_title="percentage distribution",
                      y_axis_title="concentration [mg/mL]",
                      x_axis_title="",
                      labels_bars=["Lean\nfemale", "Lean\nmale", "Obese\nfemale", "Obese\nmale"],
					  rotation=90)
# optional
# plt.show()
# plt.clf()
</pre>
