import streamlit as st


glossary = {
    "General Terms": {
        "Nation": """Nationality of the player:
        - Records in international play at senior level.
        - Youth level.
        - Citizenship from Wikipedia.
        - Birthplace when available.""",
        "Pos": """Position most commonly played by the player:
        - GK: Goalkeepers
        - DF: Defenders
        - MF: Midfielders
        - FW: Forwards""",
        "Comp": "Competition: Number next to competition states the level in the country's league pyramid.",
        "Age": """Current age:
        - Age at season start.
        - Given on August 1 for winter leagues and February 1 for summer leagues.""",
        "Born": "Year of birth"
    },
    "Playing Time": {
        "MP": "Matches Played: Matches played by the player or squad.",
        "Starts": "Game or games started by player.",
        "Min": "Minutes played.",
        "90s": "90s Played: Minutes played divided by 90."
    },
    "Standard Metrics": {
        "Gls": "Goals: Goals scored or allowed.",
        "Sh": "Shots Total: Does not include penalty kicks.",
        "SoT": "Shots on Target: Does not include penalty kicks.",
        "SoT%": """Shots on Target %:
        - Percentage of shots that are on target.
        - Minimum 0.395 shots per squad game to qualify as a leader.""",
        "Sh/90": "Shots Total/90: Shots total per 90 minutes.",
        "G/SoT": """Goals/Shot on Target:
        - Goals per shot on target.
        - Minimum 0.111 shots on target per squad game to qualify as a leader.""",
    },
    "Expected Metrics": {
        "xG": """xG: Expected Goals:
        - xG totals include penalty kicks but do not include penalty shootouts.
        - Provided by Opta.""",
        "npxG": "Non-Penalty xG: Expected goals excluding penalty kicks.",
        "G-xG": """Goals - xG:
        - Goals minus Expected Goals.
        - Provided by Opta.""",
        "np:G-xG": "Non-Penalty Goals minus Non-Penalty Expected Goals."
    },
    "Passing Metrics": {
        "Cmp": "Passes Completed: Includes live ball passes, corner kicks, throw-ins, free kicks, and goal kicks.",
        "Att": "Passes Attempted.",
        "Cmp%": "Pass Completion %.",
        "TotDist": "Total Passing Distance: Total distance, in yards, of completed passes.",
        "PrgDist": """Progressive Passing Distance:
        - Total distance, in yards, of completed passes towards the opponent's goal.""",
        "Short": {
            "Cmp": "Passes Completed (Short): Passes between 5 and 15 yards.",
            "Att": "Passes Attempted (Short): Passes between 5 and 15 yards.",
            "Cmp%": "Pass Completion % (Short): Passes between 5 and 15 yards."
        },
        "Medium": {
            "Cmp": "Passes Completed (Medium): Passes between 15 and 30 yards.",
            "Att": "Passes Attempted (Medium): Passes between 15 and 30 yards.",
            "Cmp%": "Pass Completion % (Medium): Passes between 15 and 30 yards."
        },
        "Long": {
            "Cmp": "Passes Completed (Long): Passes longer than 30 yards.",
            "Att": "Passes Attempted (Long): Passes longer than 30 yards.",
            "Cmp%": "Pass Completion % (Long): Passes longer than 30 yards."
        }
    },
    "Shot-Creating Actions": {
        "SCA": """Shot-Creating Actions:
        - The two offensive actions directly leading to a shot, such as passes, take-ons, and drawing fouls.""",
        "SCA90": "Shot-Creating Actions per 90 minutes.",
        "PassLive": "SCA (Live-ball Pass): Completed live-ball passes that lead to a shot attempt.",
        "PassDead": "SCA (Dead-ball Pass): Completed dead-ball passes that lead to a shot attempt."
    },
    "Goal-Creating Actions": {
        "GCA": """Goal-Creating Actions:
        - The two offensive actions directly leading to a goal, such as passes, take-ons, and drawing fouls.""",
        "GCA90": "Goal-Creating Actions per 90 minutes.",
        "PassLive": "GCA (Live-ball Pass): Completed live-ball passes that lead to a goal."
    },
}

# Streamlit app
st.title("Definitions")

# Render the glossary in collapsible sections
for section, terms in glossary.items():
    with st.expander(section):
        for term, definition in terms.items():
            if isinstance(definition, dict):  # For nested terms
                st.markdown(f"### {term}")
                for sub_term, sub_definition in definition.items():
                    st.markdown(f"**{sub_term}**: {sub_definition}")
            else:
                st.markdown(f"**{term}**: {definition}")

