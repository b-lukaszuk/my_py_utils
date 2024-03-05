import pandas as pd

df = pd.read_csv("./listOfJournals.csv")

# columns with discipline names:
# 302 - nauki farmaceutyczne; 303- nauki medyczne
disciplinesAnd = ["303"]
keywordsIncludeOr = [
    "diabet",
    "obes",
    "molecul",
    "lipid",
    "adipose",
    "disease",
]
keywordsExcludeOr = ["ame"]


def isDiscipline(row, disciplinesAnd=disciplinesAnd):
    bothOK = True
    for discipline in disciplinesAnd:
        if type(row[discipline]) == str:
            bothOK = bothOK and row[discipline].strip() == "x"
    return bothOK


def isOneOfTheKeywords(row, keywordsOr=keywordsIncludeOr):
    for keyword in keywordsOr:
        if keyword in str(row["tytul1"]).lower():
            return True
    for keyword in keywordsOr:
        if keyword in str(row["tytul2"]).lower():
            return True
    return False


def isOneOfExcludedKeywords(row, keywords=keywordsExcludeOr):
    return isOneOfTheKeywords(row, keywords)


def areJounalTitleCriteriaFullfilled(row):
    return isOneOfTheKeywords(row) and not isOneOfExcludedKeywords(row)


###############################################################################
#                                    query1                                   #
#           MNISW: 140, discipline: nauki medyczne i farmaceutyczne           #
###############################################################################
df140_mnisw = df[df["Punkty"] == 140]
rowsDisciplinesTrue = list(df140_mnisw.apply(isDiscipline, axis=1))
df140_mnisw_disciplines = df140_mnisw[rowsDisciplinesTrue]
rowsKeywordsOK = list(
    df140_mnisw_disciplines.apply(areJounalTitleCriteriaFullfilled, axis=1)
)
df140_mnisw_disciplines_keywords = df140_mnisw_disciplines[rowsKeywordsOK]
df140_mnisw_disciplines_keywords.to_csv(
    "./journals_candidates_query1.csv", index=False, header=True
)
