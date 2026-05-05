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
# Centralizing all UI text to support multiple languages
TRANSLATIONS = {
    "RO": {
        "sidebar_title": "SenticGuard Web v3.1",
        "lang_select": "Alege Limba / Select Language",
        "main_title": "SenticGuard AI",
        "sub_title": "Integritate Media și Analiză Deep",
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
            "CLICKBAIT": "Creat special pentru a forța click-ul.",
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
            "CLICKBAIT": "Specifically crafted to force user clicks.",
            "CONFLICTUAL": "Highlights disputes or social tensions.",
            "INFORMATIV": "Useful content, guides or explanations.",
            "OPINIE": "Subjective viewpoint or personal analysis."
        }
    }
}

# --- 3. LANGUAGE SELECTION ---
# Placing the language toggle at the top of the sidebar
with st.sidebar:
    st.title(TRANSLATIONS["EN"]["sidebar_title"]) # Title is static or from dict
    lang = st.selectbox("Language / Limbă", ["RO", "EN"], index=0)
    T = TRANSLATIONS[lang] # Current language dictionary helper
    st.markdown("---")

# --- 4. CATEGORY DEFINITIONS (COLORS) ---
CATEGORIES = {
    "OBIECTIV": "#10b981",
    "ALARMIST": "#ef4444",
    "CLICKBAIT": "#f59e0b",
    "CONFLICTUAL": "#8b5cf6",
    "INFORMATIV": "#3b82f6",
    "OPINIE": "#64748b"
}

# --- 5. CUSTOM UI STYLING (CSS) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}
    .main-card {{ background-color: #ffffff; padding: 25px; border-radius: 12px; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); margin-bottom: 20px; }}
    .verdict-badge {{ display: inline-block; padding: 4px 12px; border-radius: 6px; color: white; font-size: 14px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 10px; }}
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
    """Helper to run inference on input text."""
    if not text or not cls_pipeline:
        return None
    prediction = cls_pipeline(text.strip()[:512])[0]
    return {
        "label": prediction['label'],
        "score": float(prediction['score']),
        "color": CATEGORIES.get(prediction['label'], "#64748b"),
        "desc": T["categories"].get(prediction['label'], "")
    }

# --- 7. USER INTERFACE ---
st.title(T["main_title"])
st.markdown(f"#### {T['sub_title']}")

with st.container():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    input_mode = st.tabs([T["tab_link"], T["tab_manual"]])
    
    titlu_analiza = ""
    text_analiza = ""

    with input_mode[0]:
        url = st.text_input(T["url_label"], placeholder="https://...", key="url_input")
        if url:
            try:
                config = Config()
                config.browser_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
                article = Article(url, config=config)
                article.download()
                article.parse()
                titlu_analiza = article.title
                text_analiza = article.text
                if titlu_analiza:
                    st.success(f"{T['success_load']} {titlu_analiza}")
            except Exception as e:
                st.error(f"{T['error_load']} {e}")

    with input_mode[1]:
        manual_entry = st.text_area(T["manual_label"], height=100, key="manual_input")
        if manual_entry:
            titlu_analiza = manual_entry
    
    c1, c2 = st.columns([1, 5])
    with c1:
        start_analysis = st.button(T["analyze_btn"], type="primary", use_container_width=True)
    with c2:
        if st.button(T["reset_btn"], type="secondary"):
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- 8. RESULTS ---
if start_analysis:
    if not titlu_analiza:
        st.warning(T["warn_no_input"])
    else:
        with st.spinner('AI analysis...'):
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
                    col1, col2 = st.columns(2)
                    with col1: st.metric(T["tab_manual"], res_titlu['label'])
                    with col2: st.metric("Deep Analysis", res_content['label'])
                    
                    if res_titlu['label'] != res_content['label']:
                        st.warning(T["mismatch"])
                    else:
                        st.info(T["match"])

# --- 9. SIDEBAR LEGEND (Dynamic) ---
with st.sidebar:
    for cat, color in CATEGORIES.items():
        st.markdown(f"""
        <div style="margin-bottom: 15px;">
            <span style="color:{color}; font-weight:bold;">{cat}</span><br>
            <small style="color:#64748b;">{T['categories'].get(cat, "")}</small>
        </div>
        """, unsafe_allow_html=True)
