import streamlit as st
import random
from transformers import pipeline
from newspaper import Article, Config
from senticguard_translations import TRANSLATIONS

# --- 1. CONFIGURATION & CONSTANTS ---
# Tune the algorithm globally
WEIGHT_CONTENT = 0.7 
WEIGHT_TITLE = 0.3

st.set_page_config(
    page_title="SenticGuard AI", 
    page_icon="🛡️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. LANGUAGE SELECTION & SESSION STATE ---
if 'reset_key' not in st.session_state:
    st.session_state.reset_key = 0

with st.sidebar:
    if 'lang_idx' not in st.session_state:
        st.session_state.lang_idx = 0
        
    st.title("SenticGuard Web v3.1")
    lang = st.selectbox("Alege Limba / Select Language", ["RO", "EN"], index=st.session_state.lang_idx)
    T = TRANSLATIONS[lang]
    st.markdown("---")

# --- 3. CATEGORY COLORS DEFINITIONS ---
CATEGORIES = {
    "OBIECTIV": "#10b981",
    "ALARMIST": "#ef4444",
    "SENZATIONAL": "#f59e0b",
    "CONFLICTUAL": "#8b5cf6",
    "INFORMATIV": "#3b82f6",
    "OPINIE": "#64748b"
}

# --- 4. UI STYLING ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}
    .verdict-card {{
        background: white; border: 1px solid #e2e8f0; padding: 25px; 
        border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }}
    .verdict-badge {{ 
        display: inline-block; padding: 4px 12px; border-radius: 6px; 
        color: white; font-size: 13px; font-weight: 700; 
        text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 15px; 
    }}
    </style>
""", unsafe_allow_html=True)

# --- 5. MODEL INITIALIZATION & LOGIC ---
@st.cache_resource
def load_model():
    """Load the Transformer model from HuggingFace Hub."""
    model_path = "florin-lupsa/NewsAnalyzer" 
    try:
        return pipeline("text-classification", model=model_path, tokenizer=model_path)
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

cls_pipeline = load_model()

def analyze_text(text):
    """Run inference on a single string and return detailed classification data."""
    if not text or not cls_pipeline:
        return None
    # Truncate text to 512 tokens for model compatibility
    prediction = cls_pipeline(text.strip()[:512])[0]
    label = prediction['label']
    return {
        "label": label,
        "score": float(prediction['score']),
        "color": CATEGORIES.get(label, "#64748b"),
        "desc": T["categories"].get(label, "")
    }

def get_final_verdict(res_titlu, res_content):
    """
    Hybrid Algorithm: Combines title and content scores using internal weights.
    Selects a conversational phrase based on confidence levels and match/mismatch status.
    """
    if not res_content:
        # Case for Manual Mode or missing content
        label_v = T["labels_map"].get(res_titlu['label'], res_titlu['label'])
        phrase = random.choice(T["phrases"]["match_high"]).format(label_v=label_v)
        res = res_titlu.copy()
        res['explanation'] = phrase
        return res
    
    # 1. Weighted score calculation
    score_final_c = res_content['score'] * WEIGHT_CONTENT
    score_final_t = res_titlu['score'] * WEIGHT_TITLE
    
    # 2. Determine dominant label
    if score_final_c >= score_final_t:
        verdict_final = res_content.copy()
        # Visual boost for combined certainty
        verdict_final['score'] = score_final_c + (res_titlu['score'] * 0.1) 
    else:
        verdict_final = res_titlu.copy()
        verdict_final['score'] = score_final_t + (res_content['score'] * 0.1)

    # 3. Prepare grammatical labels for phrase interpolation
    label_v_str = T["labels_map"].get(verdict_final['label'], verdict_final['label'])
    label_s_str = T["labels_map"].get(res_titlu['label'] if score_final_c >= score_final_t else res_content['label'])

    # 4. Phrase category selection logic
    is_match = res_titlu['label'] == res_content['label']
    is_high = verdict_final['score'] > 0.85
    
    if is_match:
        category = "match_high" if is_high else "match_low"
    else:
        category = "mismatch_high" if is_high else "mismatch_low"
    
    # 5. Pick a random conversational template
    phrase_template = random.choice(T["phrases"][category])
    verdict_final['explanation'] = phrase_template.format(label_v=label_v_str, label_s=label_s_str)
    
    return verdict_final

# --- 6. USER INTERFACE ---
st.title(T["main_title"])

col_header, col_logo = st.columns([4, 1])
with col_header:
    st.markdown(f"#### {T['sub_title']}")
    st.markdown(f'<p style="font-size: 0.95rem; color: #475569;">{T["system_desc"]}</p>', unsafe_allow_html=True)
with col_logo:
    st.image("https://raw.githubusercontent.com/florinlupsatataru-git/SenticGuard/main/icon.png", width=100)

st.markdown("<br>", unsafe_allow_html=True)

analysis_mode = st.radio("Source:", [T["tab_link"], T["tab_manual"]], horizontal=True, label_visibility="collapsed")

with st.container():
    if analysis_mode == T["tab_link"]:
        input_data = st.text_input(T["url_label"], placeholder="https://...", key=f"url_{st.session_state.reset_key}")
    else:
        input_data = st.text_area(T["manual_label"], height=100, key=f"manual_{st.session_state.reset_key}")
    
    c1, c2 = st.columns([1, 5])
    with c1:
        analyze_clicked = st.button(T["analyze_btn"], type="primary", use_container_width=True)
    with c2:
        if st.button(T["reset_btn"], type="secondary"):
            st.session_state.reset_key += 1
            st.rerun()

# --- 7. RESULTS PROCESSING ---
if analyze_clicked:
    titlu_analiza = ""
    text_analiza = ""

    if analysis_mode == T["tab_link"] and input_data:
        try:
            with st.spinner('Scraping article...'):
                config = Config()
                config.browser_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...'
                article = Article(input_data, config=config)
                article.download(); article.parse()
                titlu_analiza = article.title
                text_analiza = article.text
        except Exception as e:
            st.error(f"{T['error_load']} {e}")
    elif analysis_mode == T["tab_manual"] and input_data:
        titlu_analiza = input_data

    if not titlu_analiza:
        st.warning(T["warn_no_input"])
    else:
        res_titlu = analyze_text(titlu_analiza)
        res_content = analyze_text(text_analiza) if text_analiza else None
        
        # Calculate verdict using internal weights
        verdict_final = get_final_verdict(res_titlu, res_content)

        # MAIN CARD DISPLAY (Human-Readable)
        st.markdown(f"""
            <div class="verdict-card" style="border-top: 5px solid {verdict_final['color']};">
                <div class="verdict-badge" style="background-color: {verdict_final['color']};">
                    {verdict_final['label']}
                </div>
                <p style="font-size: 1.15rem; color: #1e293b; font-weight: 500; line-height: 1.6; margin-bottom: 0;">
                    {verdict_final['explanation']}
                </p>
            </div>
        """, unsafe_allow_html=True)

        # TECHNICAL DETAILS (Expander)
        with st.expander(T['deep_title']):
            st.markdown(f"**{T['manual_label']}:** {titlu_analiza}")
            st.divider()
            
            col_r1, col_r2 = st.columns(2)
            with col_r1: 
                st.metric(T["tech_manual_label"], res_titlu['label'])
                st.progress(res_titlu['score'], text=f"{T['confidence']} {res_titlu['score']:.2%}")
            
            with col_r2: 
                if res_content:
                    st.metric(T["tech_content_label"], res_content['label'])
                    st.progress(res_content['score'], text=f"{T['confidence']} {res_content['score']:.2%}")
                else:
                    st.info(T["tech_no_content"])
            
            st.divider()
            st.write(f"**{T['tech_final_label']}** {verdict_final['score']:.2%}")
            st.caption(f"{T['tech_config_label']} {WEIGHT_CONTENT*100:.0f}% content / {WEIGHT_TITLE*100:.0f}% title")

# --- 8. SIDEBAR LEGEND ---
with st.sidebar:
    st.markdown("---")
    for cat, color in CATEGORIES.items():
        st.markdown(f'<div style="margin-bottom: 12px;"><span style="color:{color}; font-weight:bold; font-size:13px;">{cat}</span><br><small style="color:#64748b; line-height:1.2;">{T["categories"].get(cat, "")}</small></div>', unsafe_allow_html=True)
