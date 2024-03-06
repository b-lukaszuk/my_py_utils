import pandas as pd

df = pd.read_csv("./listOfJournals.csv")
dfIfPoints = pd.read_csv("./if_list.csv", sep=";")

# columns with discipline names (check it with listOfJournals.csv file):
# 301 - nauki farmaceutyczne; 302- nauki medyczne
disciplinesAnd = ["302"]
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
        if keyword in str(row["Tytuł 1"]).lower():
            return True
    for keyword in keywordsOr:
        if keyword in str(row["Tytuł 2"]).lower():
            return True
    return False


def isOneOfExcludedKeywords(row, keywords=keywordsExcludeOr):
    return isOneOfTheKeywords(row, keywords)


def areJounalTitleCriteriaFullfilled(row):
    return isOneOfTheKeywords(row) and not isOneOfExcludedKeywords(row)


def isMenPoints(row, pts):
    return row["Punktacja"] in pts


def rmCharFromText(text, char):
    return text.strip().replace(char, "")


def getIndOfIssn(colWithIssns, issn):
    for i, colIssn in enumerate(colWithIssns):
        if rmCharFromText(str(issn), "-") in colIssn:
            return i
    return -99


def getIFsForIssns(dfIfs, issns):
    colWithIssns = list(dfIfs["Issn"])
    ifs = []
    for issn in issns:
        ifs.append(dfIfs.iloc[
            getIndOfIssn(colWithIssns, issn), ]['Cites / Doc. (2years)'])
    return ifs


###############################################################################
#                                    query1                                   #
#           MNISW: 140, discipline: nauki medyczne i farmaceutyczne           #
###############################################################################
df_w_men_pts = df[list(df.apply(isMenPoints, axis=1, pts=[140, 100]))]
rowsDisciplinesTrue = list(df_w_men_pts.apply(isDiscipline, axis=1))
df_w_men_pts_and_disciplines = df_w_men_pts[rowsDisciplinesTrue]
rowsKeywordsOK = list(
    df_w_men_pts_and_disciplines.apply(areJounalTitleCriteriaFullfilled,
                                       axis=1)
)
df_w_men_pts_and_disciplines_and_keywords = df_w_men_pts_and_disciplines[
    rowsKeywordsOK]

ifs = getIFsForIssns(
    dfIfPoints, list(df_w_men_pts_and_disciplines_and_keywords["issn"]))

df_w_men_pts_and_disciplines_and_keywords.insert(loc=1, column="IF", value=ifs)

df_w_men_pts_and_disciplines_and_keywords.to_csv(
    "./journals_candidates_query1.csv", index=False, header=True
)
