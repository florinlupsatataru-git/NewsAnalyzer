import streamlit as st
import feedparser
import pandas as pd
import gdown
import os
from streamlit_gsheets import GSheetsConnection
from transformers import pipeline

# --- 1. CONFIGURAȚIE CATEGORII ---
# This list must correspond EXACTLY to the label_map in the training script
CATEGORIES_MAP = {
    "OBIECTIV": 0,
    "ALARMIST": 1,
    "SENZATIONAL": 2,
    "CONFLICTUAL": 3,
    "INFORMATIV": 4,
    "OPINIE": 5
}
CATEGORII_LIST = list(CATEGORIES_MAP.keys())

# --- 2. LOGIN AND SECURITY ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

def login():
    st.title("🔐 SenticGuard Admin Panel")
    parola = st.text_input("Introdu parola de administrator", type="password")
    if st.button("Log In"):
        if parola == st.secrets["ADMIN_PASSWORD"]:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Parolă incorectă")

if not st.session_state["authenticated"]:
    login()
    st.stop()

# --- 3. MODEL LOADING ---
@st.cache_resource
def load_classifier():
    save_path = "./model_temp"
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    # Updated Google Drive IDs for the new model (config.json)
    files = {
        "config.json": "1kKvuBeOMMiIXF8_UtP3zoI6lxi6RPvo8",
        "model.safetensors": "1Nrnp84om-EKrNDDdeS8JcYTArwOwusF7", 
        "tokenizer_config.json": "1If1PxDO6I9-ch55fgqxqFl9X0AHtWwjY",
        "tokenizer.json": "1e1WkWXewonur2dTuPekixV-liMQhigQi"
    }
    
    try:
        for name, file_id in files.items():
            local_file = os.path.join(save_path, name)
            if not os.path.exists(local_file):
                file_url = f'https://drive.google.com/uc?id={file_id}'
                gdown.download(file_url, local_file, quiet=True)
        
        # The model will use id2label defined in config.json
        return pipeline("text-classification", model=save_path, tokenizer=save_path)
    except Exception as e:
        st.error(f"Eroare la descărcarea modelului: {e}")
        return None

# --- 4. ADMIN USER INTERFACE ---
st.title("🚀 Colectare & Validare AI (v2.0 - 6 Categorii)")

RSS_FEEDS = {
    "Mediafax": "https://www.mediafax.ro/rss",
    "Hotnews": "https://www.hotnews.ro/rss",
    "Digi24": "https://www.digi24.ro/rss",
    "G4Media": "https://www.g4media.ro/feed",
    "Libertatea": "https://www.libertatea.ro/feed",
    "Stirile ProTV": "https://stirileprotv.ro/rss",
    "Antena 3": "https://www.antena3.ro/rss"
}

sursa = st.selectbox("Alege sursa de știri:", list(RSS_FEEDS.keys()))

if st.button("Aduceți titluri noi"):
    with st.spinner('AI-ul clasifică știrile pe cele 6 categorii...'):
        feed = feedparser.parse(RSS_FEEDS[sursa])
        classifier = load_classifier()
        
        new_data = []
        for entry in feed.entries[:30]:
            label_sugerat = "OBIECTIV"
            scor_ai = 0.0
            
            if classifier:
                rezultat = classifier(entry.title)[0]
                label_sugerat = rezultat['label'] # Returnează direct numele (ex: "ALARMIST")
                scor_ai = rezultat['score']
            
            new_data.append({
                "text": entry.title,
                "ai_label": label_sugerat,
                "ai_score": scor_ai
            })
        
        st.session_state.temp_df = pd.DataFrame(new_data)

# --- 5. ZONA DE VALIDARE ---
if "temp_df" in st.session_state:
    st.write("### 📝 Analiză și Validare Manuală")
    st.info("Verifică sugestia AI și corectează dacă este necesar înainte de a salva.")
    
    etichete_validate = []
    
    for index, row in st.session_state.temp_df.iterrows():
        st.markdown(f"**Titlu:** {row['text']}")
        
        col1, col2 = st.columns([0.7, 0.3])
        
        with col1:
            # Selector pentru cele 6 categorii, cu index presetat de AI
            index_default = CATEGORII_LIST.index(row['ai_label']) if row['ai_label'] in CATEGORII_LIST else 0
            
            alegere = st.selectbox(
                f"Categorie pentru titlul {index}:",
                options=CATEGORII_LIST,
                index=index_default,
                key=f"select_{index}",
                label_visibility="collapsed"
            )
        
        with col2:
            conf_color = "🟢" if row['ai_score'] > 0.8 else "🟡" if row['ai_score'] > 0.6 else "🔴"
            st.write(f"Sugestie AI: **{row['ai_label']}** ({conf_color} {row['ai_score']:.1%})")
        
        # We save the number corresponding to the chosen category (0-5)
        etichete_validate.append(CATEGORIES_MAP[alegere])
        st.divider()

    # --- 6. SAVE TO GOOGLE SHEETS ---
    if st.button("💾 Confirmă și Salvează în Dataset", type="primary"):
        try:
            conn = st.connection("gsheets", type=GSheetsConnection)
            existing_df = conn.read()
            
            to_save = pd.DataFrame({
                "text": st.session_state.temp_df["text"],
                "label": etichete_validate
            })
            
            updated_df = pd.concat([existing_df, to_save], ignore_index=True)
            conn.update(data=updated_df)
            
            st.success(f"✅ Am adăugat {len(to_save)} titluri noi în Google Sheets!")
            
            # Clear the session to force a new feed on the next run
            del st.session_state.temp_df
            st.cache_resource.clear()
            st.rerun() # Refresh for clean interface
            
        except Exception as e:
            st.error(f"Eroare la salvare: {e}")

# --- SIDEBAR: Manual add ---
st.sidebar.title("➕ Adăugare Manuală")
manual_text = st.sidebar.text_area("Titlu știre nouă:", key="manual_text_input")
manual_cat = st.sidebar.selectbox("Categorie:", CATEGORII_LIST)

if st.sidebar.button("Salvează Titlu"):
    if manual_text:
        try:
            conn = st.connection("gsheets", type=GSheetsConnection)
            existing_df = conn.read()
            
            new_row = pd.DataFrame({"text": [manual_text], "label": [CATEGORIES_MAP[manual_cat]]})
            updated_df = pd.concat([existing_df, new_row], ignore_index=True)
            conn.update(data=updated_df)
            
            st.sidebar.success("Titlu salvat!")
            # Reset manual add
            st.session_state["manual_text_input"] = ""
            st.rerun()
        except Exception as e:
            st.sidebar.error(f"Eroare: {e}")
