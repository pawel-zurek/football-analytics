import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import pi


st.set_page_config(
   page_title="QuickScout",
)


# Load data
df1 = pd.read_csv('/Users/pawel/Documents/Python/football-analytics/QuickScout/fbref_final.csv')




# Streamlit title
st.title("QuickScout: a tool to look up similar players with a radar chart")
st.divider()


# Dropdown menu to select a player
default_player = df1["Player"].iloc[1827]  # Robert Lewandowski as the default player
selected_player = st.selectbox("Select a player:", df1["Player"], index=df1["Player"].tolist().index(default_player))
position = df1.loc[df1["Player"] == selected_player, 'Pos'].iloc[0]
st.write("")
st.write("")


# Presets for positions that generate default statistics for selection
default_stats_forward = ['Standard Gls', 'Expected npxG', 'Standard SoT%', 'Standard Sh/90', 'Receiving PrgR', 'Touches Att 3rd', 'Aerial Duels Won%']
default_stats_midfielders = ['Total Cmp%', 'Expected xA', 'PrgP', 'Pass Types TB', 'Pass Types Crs', 'SCA SCA90', 'Touches Mid 3rd']
default_stats_defenders = ['Total Cmp%', 'Touches Def 3rd', 'Long Cmp', 'Challenges Tkl%', 'Blocks Sh', 'Tkl+Int', 'Clr']


if position[0:2] == 'FW':
   default_stats = default_stats_forward
elif position[0:2] == 'MF':
   default_stats = default_stats_midfielders
else:
   default_stats = default_stats_defenders


# Sidebar for statistic selection
selected_stats = st.sidebar.multiselect(
   "Select Statistics: choose at least 3",
   options=df1.columns[8:],  # Exclude descriptive columns and age
   default=default_stats
)


# Checkbox for finding hidden gems
checkbox_value = st.sidebar.checkbox("Find hidden gems", value=False)


# Some safeguards from crashing the plot
if len(selected_stats) == 2:
   selected_stats = ['Playing Time Min'] + selected_stats
elif len(selected_stats) == 1:
   selected_stats = ['Playing Time Min', 'Playing Time 90s'] + selected_stats
elif len(selected_stats) == 0:
   selected_stats = ['Playing Time Min', 'Playing Time 90s', 'Playing Time Starts'] + selected_stats
else:
   selected_stats = selected_stats


# Data used for comparing players and building the chart
if checkbox_value:
   percentile_50 = df1["Playing Time Min"].quantile(0.50)
   filtered_df = df1[df1["Playing Time Min"] < percentile_50]
   if selected_player not in filtered_df["Player"].values:
       selected_player_row = df1[df1["Player"] == selected_player]
       filtered_df = pd.concat([filtered_df, selected_player_row])
   df1 = filtered_df.reset_index(drop=True)
   data = df1[['Player'] + selected_stats]
else:
   data = df1[['Player'] + selected_stats]




Attributes = list(data)[1:]
AttNo = len(Attributes)




def find_most_similar_player(selected_player, stats_df):
   # Drop rows with NaN values in numeric columns
   stats_df = stats_df.dropna(subset=stats_df.columns[1:])


   # Rank players by percentiles for each stat
   percentile_df = stats_df.copy()
   for col in stats_df.columns[1:]:  # Skip the "Player" column
       percentile_df[col] = stats_df[col].rank(pct=True) * 100


   # Extract the percentiles of the selected player
   selected_stats = percentile_df.loc[percentile_df["Player"] == selected_player].iloc[:, 1:].values.flatten()


   # Check if selected_stats is valid
   if selected_stats.size == 0:
       raise ValueError(f"No valid data found for player {selected_player}.")


   # Compute the sum of squared differences for all other players
   other_players = percentile_df[percentile_df["Player"] != selected_player]
   differences = other_players.iloc[:, 1:].apply(
       lambda row: np.sum((row.to_numpy() - selected_stats) ** 2), axis=1
   )


   # Find the index of the most similar player
   most_similar_index = differences.idxmin()


   return other_players.loc[most_similar_index, "Player"]




def find_hidden_gems(selected_player, stats_df):
   import numpy as np


   # Drop rows with NaN values in numeric columns
   stats_df = stats_df.dropna(subset=stats_df.columns[1:])


   # Rank players by percentiles for each stat
   percentile_df = stats_df.copy()
   for col in stats_df.columns[1:]:  # Skip the "Player" column
       percentile_df[col] = stats_df[col].rank(pct=True) * 100


   # Normalize percentile scores for each player by dividing by their maximum value
   normalized_df = percentile_df.copy()
   for index, row in percentile_df.iloc[:, 1:].iterrows():
       max_val = row.max()
       if max_val > 0:  # Avoid division by zero
           normalized_df.iloc[index, 1:] = (row / max_val).values


   # Extract the normalized stats of the selected player
   selected_stats = normalized_df.loc[normalized_df["Player"] == selected_player].iloc[:, 1:].values.flatten()


   # Check if selected_stats is valid
   if selected_stats.size == 0:
       raise ValueError(f"No valid data found for player {selected_player}.")


   # Compute the sum of squared differences for normalized percentiles
   other_players = normalized_df[normalized_df["Player"] != selected_player]
   differences = other_players.iloc[:, 1:].apply(
       lambda row: np.sum((row.to_numpy() - selected_stats) ** 2), axis=1
   )


   # Find the index of the most similar player
   most_similar_index = differences.idxmin()


   return other_players.loc[most_similar_index, "Player"]




def plot_radar_chart(stats_df, player1, player2):
   # Convert all stats to percentiles
   percentile_data = data.copy()
   for col in data.columns[1:]:  # Skip the "Player" column
       percentile_data[col] = data[col].rank(pct=True) * 100


   # Find the values and angles for Player1 (percentiles)
   player_finder = percentile_data.loc[percentile_data["Player"] == selected_player]
   values = player_finder.iloc[0][1:].tolist()
   values += values[:1]  # Close the radar chart


   angles = [n / float(AttNo) * 2 * pi for n in range(AttNo)]
   angles += angles[:1]  # Close the radar chart


   # Find the values and angles for Player2 (percentiles)
   player_finder2 = percentile_data.loc[percentile_data["Player"] == most_similar_player]
   values2 = player_finder2.iloc[0][1:].tolist()
   values2 += values2[:1]  # Close the radar chart


   # Create the chart with the specified background color
   fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True), facecolor="#0e1117")
   ax.set_facecolor("#0e1117")


   # Add attribute labels and customize colors
   plt.xticks(angles[:-1], Attributes, color="white", fontsize=10)
   plt.yticks(color="white", fontsize=8)
   ax.spines['polar'].set_color('white')


   # Plot Player1
   ax.plot(angles, values, color="teal", linewidth=2, label=player1)
   ax.fill(angles, values, color="teal", alpha=0.3)


   # Plot Player2
   ax.plot(angles, values2, color="red", linewidth=2, label=player2)
   ax.fill(angles, values2, color="red", alpha=0.3)


   # Add legend
   ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.2), labelcolor="#0e1117", fontsize=10)


   return fig




# Find the most similar player
if selected_player:
   if checkbox_value:
       most_similar_player = find_hidden_gems(selected_player, data)
   else:
       most_similar_player = find_most_similar_player(selected_player, data)
   bio = df1.loc[df1["Player"] == selected_player][['Nation', 'Pos', 'Squad', 'Comp']]
   bio['Nation'] = bio['Nation'].apply(lambda x: x[3:] if isinstance(x, str) else x)
   bio['Comp'] = bio['Comp'].apply(lambda x: x[3:] if isinstance(x, str) else x)
   st.write("### Player Information:")
   st.markdown(bio.to_html(index=False), unsafe_allow_html=True)
   st.write("")
   st.write("")
   st.write(f"### The most similar player to **{selected_player}** is:")
   st.write(f"## **{most_similar_player}**")
   bio2 = df1.loc[df1["Player"] == most_similar_player][['Nation', 'Pos', 'Squad', 'Comp']]
   bio2['Nation'] = bio2['Nation'].apply(lambda x: x[3:] if isinstance(x, str) else x)
   bio2['Comp'] = bio2['Comp'].apply(lambda x: x[3:] if isinstance(x, str) else x)
   st.markdown(bio2.to_html(index=False), unsafe_allow_html=True)
   st.divider()


   # Display radar chart comparison
   st.write("## Stats Visualization (Radar Chart)")
   radar_fig = plot_radar_chart(data, selected_player, most_similar_player)
   st.pyplot(radar_fig)

