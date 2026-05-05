import streamlit as st
from transformers import pipeline
from newspaper import Article, Config

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="SenticGuard AI", 
    page_icon="🛡️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. MULTILINGUAL DICTIONARY ---
TRANSLATIONS = {
    "RO": {
        "sidebar_title": "SenticGuard Web v3.1",
        "lang_select": "Alege Limba / Select Language",
        "main_title": "SenticGuard AI",
        "sub_title": "Integritate Media și Analiză Deep",
        "system_desc": "SenticGuard este un sistem inteligent conceput pentru a identifica tiparele de manipulare emoțională, senzaționalism și dezinformare din fluxurile de știri din România, utilizând tehnologia NLP.",
        "tab_link": "Link Articol",
        "tab_manual": "Text Manual",
        "url_label": "URL Articol:",
        "manual_label": "Titlu / Paragraf:",
        "analyze_btn": "Analizează",
        "reset_btn": "Reset",
        "success_load": "Articol detectat: ",
        "error_load": "Eroare de acces: ",
        "warn_no_input": "Te rugăm să introduci un URL sau text manual.",
        "confidence": "ÎNCREDERE MODEL:",
        "deep_title": "Deep Analysis: Titlu vs. Conținut",
        "mismatch": "Atenție: Discrepanță detectată între tonul titlului și cel al conținutului.",
        "match": "Tonul titlului corespunde cu cel al conținutului.",
        "categories": {
            "OBIECTIV": "Informație neutră, bazată pe fapte verificabile.",
            "ALARMIST": "Titlu care induce panică sau teamă exagerată.",
            "SENZATIONAL": "Creat special pentru a atrage atenția prin exagerări.",
            "CONFLICTUAL": "Subliniază dispute sau tensiuni sociale.",
            "INFORMATIV": "Conținut util, ghiduri sau explicații.",
            "OPINIE": "Punct de vedere subiectiv sau analiză."
        }
    },
    "EN": {
        "sidebar_title": "SenticGuard Web v3.1",
        "lang_select": "Select Language",
        "main_title": "SenticGuard AI",
        "sub_title": "Media Integrity & Deep Analysis",
        "system_desc": "SenticGuard is an intelligent system designed to identify patterns of emotional manipulation, sensationalism, and disinformation in Romanian news feeds using NLP technology.",
        "tab_link": "Article Link",
        "tab_manual": "Manual Text",
        "url_label": "Article URL:",
        "manual_label": "Title / Paragraph:",
        "analyze_btn": "Analyze",
        "reset_btn": "Reset",
        "success_load": "Article detected: ",
        "error_load": "Access error: ",
        "warn_no_input": "Please provide a URL or manual text.",
        "confidence": "MODEL CONFIDENCE:",
        "deep_title": "Deep Analysis: Title vs. Content",
        "mismatch": "Attention: Discrepancy detected between title and content tone.",
        "match": "Title tone matches the content tone.",
        "categories": {
            "OBIECTIV": "Neutral info, based on verifiable facts.",
            "ALARMIST": "Headlines designed to induce panic or fear.",
            "SENZATIONAL": "Content crafted to attract attention through exaggerations.",
            "CONFLICTUAL": "Highlights disputes or social tensions.",
            "INFORMATIV": "Useful content, guides or explanations.",
            "OPINIE": "Subjective viewpoint or personal analysis."
        }
    }
}

# --- 3. LANGUAGE SELECTION ---
with st.sidebar:
    st.title(TRANSLATIONS["EN"]["sidebar_title"])
    lang = st.selectbox("Language / Limbă", ["RO", "EN"], index=0)
    T = TRANSLATIONS[lang]
    st.markdown("---")

# --- 4. CATEGORY DEFINITIONS ---
CATEGORIES = {
    "OBIECTIV": "#10b981",
    "ALARMIST": "#ef4444",
    "SENZATIONAL": "#f59e0b",
    "CONFLICTUAL": "#8b5cf6",
    "INFORMATIV": "#3b82f6",
    "OPINIE": "#64748b"
}

# --- 5. CUSTOM UI STYLING ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}
    [data-testid="stVerticalBlock"] > div:has(div > .stTabs) {{
        background-color: #ffffff; padding: 25px; border-radius: 12px;
        border: 1px solid #e2e8f0; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }}
    .verdict-badge {{ 
        display: inline-block; padding: 4px 12px; border-radius: 6px; 
        color: white; font-size: 14px; font-weight: 700; 
        text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 10px; 
    }}
    </style>
""", unsafe_allow_html=True)

# --- 6. MODEL INITIALIZATION ---
@st.cache_resource
def load_model():
    model_path = "florin-lupsa/NewsAnalyzer" 
    try:
        return pipeline("text-classification", model=model_path, tokenizer=model_path)
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

cls_pipeline = load_model()

def analyze_text(text):
    if not text or not cls_pipeline:
        return None
    prediction = cls_pipeline(text.strip()[:512])[0]
    label = prediction['label']
    return {
        "label": label,
        "score": float(prediction['score']),
        "color": CATEGORIES.get(label, "#64748b"),
        "desc": T["categories"].get(label, "")
    }

# --- 7. USER INTERFACE ---
st.title(T["main_title"])

# INITIALIZE STATE
if 'reset_key' not in st.session_state:
    st.session_state.reset_key = 0

col_header, col_logo = st.columns([4, 1])
with col_header:
    st.markdown(f"#### {T['sub_title']}")
    st.markdown(f'<p style="font-size: 0.95rem; color: #475569;">{T["system_desc"]}</p>', unsafe_allow_html=True)
with col_logo:
    st.image("https://raw.githubusercontent.com/florinlupsatataru-git/SenticGuard/main/icon.png", width=100)

st.markdown("<br>", unsafe_allow_html=True)

analysis_mode = st.radio("Sursă Date:", [T["tab_link"], T["tab_manual"]], horizontal=True, label_visibility="collapsed")

with st.container():
    titlu_analiza = ""
    text_analiza = ""

    if analysis_mode == T["tab_link"]:
        url_input = st.text_input(T["url_label"], placeholder="https://...", key=f"url_{st.session_state.reset_key}")
    else:
        manual_input = st.text_area(T["manual_label"], height=100, key=f"manual_{st.session_state.reset_key}")
    
    c1, c2 = st.columns([1, 5])
    with c1:
        analyze_clicked = st.button(T["analyze_btn"], type="primary", use_container_width=True)
    with c2:
        if st.button(T["reset_btn"], type="secondary"):
            st.session_state.reset_key += 1
            st.rerun()

# --- 8. RESULTS ---
if analyze_clicked:
    if analysis_mode == T["tab_link"]:
        current_url = st.session_state.get(f"url_{st.session_state.reset_key}", "")
        if current_url:
            try:
                with st.spinner('Scraping...'):
                    config = Config()
                    config.browser_user_agent = 'Mozilla/5.0...'
                    article = Article(current_url, config=config)
                    article.download(); article.parse()
                    titlu_analiza = article.title
                    text_analiza = article.text
            except Exception as e:
                st.error(f"{T['error_load']} {e}")
    else:
        titlu_analiza = st.session_state.get(f"manual_{st.session_state.reset_key}", "")

    if not titlu_analiza:
        st.warning(T["warn_no_input"])
    else:
        res_titlu = analyze_text(titlu_analiza)
        if res_titlu:
            st.markdown(f"""
                <div style="background: white; border: 1px solid #e2e8f0; padding: 25px; border-radius: 12px; border-top: 5px solid {res_titlu['color']};">
                    <div class="verdict-badge" style="background-color: {res_titlu['color']};">
                        {res_titlu['label']}
                    </div>
                    <h3 style="margin-top: 0; color: #0f172a;">{titlu_analiza}</h3>
                    <p style="color: #64748b; font-size: 15px;">{res_titlu['desc']}</p>
                    <div style="display: flex; align-items: center; gap: 10px; margin-top: 20px;">
                        <span style="font-size: 13px; font-weight: 600; color: #94a3b8;">{T['confidence']}</span>
                        <span style="font-size: 13px; font-weight: 700; color: {res_titlu['color']};">{res_titlu['score']:.2%}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            if text_analiza:
                st.markdown("<br>", unsafe_allow_html=True)
                res_content = analyze_text(text_analiza)
                st.subheader(T["deep_title"])
                col_r1, col_r2 = st.columns(2)
                with col_r1: st.metric(T["tab_manual"], res_titlu['label'])
                with col_r2: st.metric("Deep Analysis", res_content['label'])
                
                if res_titlu['label'] != res_content['label']:
                    st.warning(T["mismatch"])
                else:
                    st.info(T["match"])

# --- 9. SIDEBAR LEGEND ---
with st.sidebar:
    for cat, color in CATEGORIES.items():
        st.markdown(f'<div style="margin-bottom: 15px;"><span style="color:{color}; font-weight:bold;">{cat}</span><br><small style="color:#64748b;">{T["categories"].get(cat, "")}</small></div>', unsafe_allow_html=True)
