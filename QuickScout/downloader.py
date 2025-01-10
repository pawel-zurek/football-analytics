import pandas as pd
import numpy as np

# Iterate over a few similar links from fbref and concat the tables into one big dataframe

base_link = 'https://fbref.com/en/comps/Big5/{}/players/Big-5-European-Leagues-Stat'
sections = ["stats","shooting", "passing", "passing_types", "gca", "defense", "possession", "misc"]

urls = [base_link.format(section) for section in sections]

df1 = pd.DataFrame()

for url in urls:
    df = pd.read_html(url)[0]
    df.columns = [' '.join(col).strip() for col in df.columns]
    df = df.reset_index(drop=True)

    new_columns = []
    for col in df.columns:
        if 'level_0' in col:
            new_col = col.split()[-1]
        else:
            new_col = col
        new_columns.append(new_col)

    df.columns = new_columns

    if 'stats' not in url:
        df.drop(columns=['Rk','Player', 'Nation', 'Pos', 'Squad', 'Comp', 'Age', 'Born', 'Matches', '90s'], inplace=True)
    else:
        df = df.iloc[:, 1:12]

    df = df.fillna(0)

    df1 = pd.concat([df1, df], axis=1)


# Drop the lines with page breaks that appear every 70-something rows
data = df1.loc[df1["Player"] != "Player"].reset_index(drop=True)

# Drop goalkeepers
data = data.loc[data["Pos"] != "GK"].reset_index(drop=True)

# Convert to floats, skip the descriptive columns
for col in data.columns[7:]:
    data[col] = data[col].astype(float)

# Find and delete duplicate column names
data = data.loc[:, ~data.columns.duplicated()]

# Keep only the row with the highest minutes played for each unique Player (transferred players appear in >1 row)
data = data.loc[data.groupby('Player')['Playing Time Min'].idxmax()]
data = data.reset_index(drop=True)


data.to_csv('fbref_final.csv')
