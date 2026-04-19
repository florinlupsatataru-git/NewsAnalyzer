import streamlit as st
import feedparser
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# Page config
st.set_page_config(page_title="SenticGuard Admin", layout="wide")

# 1. Login through Secrets
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

def login():
    st.title("🔐 SenticGuard Admin Panel")
    parola_introdusa = st.text_input("Introdu parola de administrator", type="password")
    if st.button("Log In"):
        if parola_introdusa == st.secrets["ADMIN_PASSWORD"]:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Parolă incorectă!")

if not st.session_state["authenticated"]:
    login()
    st.stop()

# 2. Admin interface
st.title("🚀 Colectare Date Training")

RSS_FEEDS = {
    "Mediafax": "https://www.mediafax.ro/rss",
    "Hotnews": "https://www.hotnews.ro/rss",
    "Ziarul Financiar": "https://www.zf.ro/rss",
    "G4Media": "https://www.g4media.ro/feed",
    "Digi24": "https://www.digi24.ro/rss"
}

sursa = st.selectbox("Alege sursa de știri:", list(RSS_FEEDS.keys()))

if st.button("Aduceți titluri noi"):
    with st.spinner('Se citesc fluxurile RSS...'):
        feed = feedparser.parse(RSS_FEEDS[sursa])
        new_data = []
        for entry in feed.entries[:40]: 
            new_data.append({"text": entry.title, "label": 0})
        
        st.session_state.temp_df = pd.DataFrame(new_data)

if "temp_df" in st.session_state:
    st.info("Schimbă '0' în '1' pentru titlurile alarmiste înainte de salvare.")
    # Tabel editabil
    edited_df = st.data_editor(st.session_state.temp_df, use_container_width=True)
    
    if st.button("💾 Salvează în Google Drive"):
        try:
            conn = st.connection("gsheets", type=GSheetsConnection)
            # Citim baza existentă
            existing_df = conn.read()
            # Combinăm
            updated_df = pd.concat([existing_df, edited_df], ignore_index=True)
            # Update în Cloud
            conn.update(data=updated_df)
            st.success(f"✅ Succes! Am adăugat {len(edited_df)} rânduri în Drive.")
            del st.session_state.temp_df # Resetăm tabelul după salvare
        except Exception as e:
            st.error(f"Eroare la comunicarea cu Google Sheets: {e}")
