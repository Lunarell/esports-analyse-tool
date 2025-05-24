
import streamlit as st
import pandas as pd
from datetime import date
import re

# ==============================
# Funktion zum Parsen von DESBL-Links (Platzhalter)
def parse_desbl_match(url):
    if "desbl.de" not in url:
        return None
    # Platzhalter-Daten
    return {
        "Datum": date.today(),
        "Team 1": "Team Alpha",
        "Team 2": "Team Beta",
        "Map": "Bank",
        "Score 1": 7,
        "Score 2": 4,
        "1. Ban Team 1": "Consulate",
        "1. Ban Team 2": "Kafe",
        "Operator-Ban T1": "Valkyrie",
        "Operator-Ban T2": "Thatcher"
    }

# ==============================
# Funktion zum Parsen von FACEIT-Links (Platzhalter)
def parse_faceit_match(url):
    if "faceit.com" not in url:
        return None
    return {
        "Datum": date.today(),
        "Team 1": "Squad A",
        "Team 2": "Squad B",
        "Map": "Oregon",
        "Score 1": 5,
        "Score 2": 7,
        "1. Ban Team 1": "Nighthaven",
        "1. Ban Team 2": "Border",
        "Operator-Ban T1": "Bandit",
        "Operator-Ban T2": "Azami"
    }

# ==============================
st.set_page_config(page_title="Esports Match Tracker", layout="centered")
st.title("🎮 Esports Match Tracker")

st.markdown("Trage ein Match manuell ein oder lade es per Link von einer Website.")

# Lokaler Matchspeicher (SessionState)
if "match_list" not in st.session_state:
    st.session_state["match_list"] = []

# ==============================
# Eingabeformular
with st.form("manual_form"):
    st.subheader("📝 Manuelle Eingabe")
    col1, col2 = st.columns(2)
    with col1:
        team1 = st.text_input("Team 1")
        team1_ban = st.text_input("1. Map-Ban Team 1")
        team1_opban = st.text_input("Operator-Ban Team 1")
        score1 = st.number_input("Score Team 1", min_value=0, max_value=10)
    with col2:
        team2 = st.text_input("Team 2")
        team2_ban = st.text_input("1. Map-Ban Team 2")
        team2_opban = st.text_input("Operator-Ban Team 2")
        score2 = st.number_input("Score Team 2", min_value=0, max_value=10)

    map_played = st.text_input("Gespielte Map")
    match_date = st.date_input("Matchdatum", date.today())
    manual_submit = st.form_submit_button("✅ Speichern")

if manual_submit:
    entry = {
        "Datum": match_date,
        "Team 1": team1,
        "Team 2": team2,
        "Map": map_played,
        "Score 1": score1,
        "Score 2": score2,
        "1. Ban Team 1": team1_ban,
        "1. Ban Team 2": team2_ban,
        "Operator-Ban T1": team1_opban,
        "Operator-Ban T2": team2_opban
    }
    st.session_state.match_list.append(entry)
    st.success("Match gespeichert!")

# ==============================
# Link-Eingabe
st.subheader("🌐 Matchdaten per Link laden")
match_url = st.text_input("Match-Link eingeben (DESBL, FACEIT, etc.)")

if st.button("🔍 Matchdaten laden"):
    match_data = None
    if "desbl.de" in match_url:
        match_data = parse_desbl_match(match_url)
    elif "faceit.com" in match_url:
        match_data = parse_faceit_match(match_url)
    else:
        st.warning("Aktuell werden nur DESBL und FACEIT Links unterstützt.")

    if match_data:
        st.session_state.match_list.append(match_data)
        st.success("✅ Matchdaten aus Link geladen und gespeichert!")
    else:
        st.error("❌ Matchdaten konnten nicht geladen werden.")

# ==============================
# Matchübersicht
if st.session_state.match_list:
    st.subheader("📊 Gespeicherte Matches")
    df = pd.DataFrame(st.session_state.match_list)
    st.dataframe(df)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 CSV herunterladen", data=csv, file_name="matchdaten.csv", mime="text/csv")
Datei gelöscht
