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
    st.write("### 📝 Etichetare Știri")
    st.info("Bifează știrile care ți se par **Alarmiste**. Cele nebifate vor fi salvate ca 'Informaționale'.")

    # List for new titles
    updated_labels = []

    # Every title with a checkbox beside
    for index, row in st.session_state.temp_df.iterrows():
        # New column for checkbox
        col1, col2 = st.columns([0.1, 0.9])
        with col1:
            is_alarmist = st.checkbox("Alarmist", key=f"check_{index}")
        with col2:
            st.write(row["text"])
        
        # Save 1 if checked, 0 otherwise
        updated_labels.append(1 if is_alarmist else 0)

    if st.button("💾 Salvează selecția în Google Drive"):
        try:
            with st.spinner('Se salvează în Drive...'):
                conn = st.connection("gsheets", type=GSheetsConnection)
                
                # Getting data ready using checked values
                to_save_df = pd.DataFrame({
                    "text": st.session_state.temp_df["text"],
                    "label": updated_labels
                })
                
                # Reading file and concatenate
                existing_df = conn.read()
                updated_df = pd.concat([existing_df, to_save_df], ignore_index=True)
                
                # Update in Cloud
                conn.update(data=updated_df)
                
                st.success(f"✅ Am salvat {len(to_save_df)} știri noi!")
                del st.session_state.temp_df
                st.rerun()
        except Exception as e:
            st.error(f"Eroare: {e}")
