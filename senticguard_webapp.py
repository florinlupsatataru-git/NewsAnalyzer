import streamlit as st
from transformers import pipeline
from newspaper import Article, Config

# --- 1. PAGE CONFIGURATION ---
# Sets the app title, icon and ensures the sidebar is visible by default
st.set_page_config(
    page_title="SenticGuard AI", 
    page_icon="🛡️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CUSTOM UI STYLING (CSS) ---
# Defines the professional look: Inter font, custom cards, and verdict badges
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    .main-card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }
    
    .verdict-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 6px;
        color: white;
        font-size: 14px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. CATEGORY DEFINITIONS ---
# Mapping the 6 labels to their respective colors and descriptions
CATEGORIES = {
    "OBIECTIV": {"color": "#10b981", "desc": "Neutral information based on verifiable facts."},
    "ALARMIST": {"color": "#ef4444", "desc": "Headlines designed to induce fear or exaggerated panic."},
    "CLICKBAIT": {"color": "#f59e0b", "desc": "Content specifically crafted to force user clicks."},
    "CONFLICTUAL": {"color": "#8b5cf6", "desc": "Highlights disputes, arguments, or social tensions."},
    "INFORMATIV": {"color": "#3b82f6", "desc": "Useful content, such as guides or practical explanations."},
    "OPINIE": {"color": "#64748b", "desc": "Subjective viewpoint or personal analysis."}
}

# --- 4. MODEL INITIALIZATION ---
# Using cache_resource to load the transformer model once and keep it in memory
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
    """Helper function to run classification and return a structured result."""
    if not text or not cls_pipeline:
        return None
    # Truncate input to 512 tokens to prevent BERT errors
    prediction = cls_pipeline(text.strip()[:512])[0]
    return {
        "label": prediction['label'],
        "score": float(prediction['score']),
        "config": CATEGORIES.get(prediction['label'], {"color": "#64748b", "desc": ""})
    }

# --- 5. USER INTERFACE ---
st.title("SenticGuard AI")
st.markdown("#### Media Integrity & Deep Analysis")

# Main Container for Input
with st.container():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    input_mode = st.tabs(["Link Articol", "Text Manual"])
    
    titlu_analiza = ""
    text_analiza = ""

    # Link Input: Scraping title and content using newspaper3k
    with input_mode[0]:
        url = st.text_input("URL Articol:", placeholder="Paste link here...", key="url_input")
        if url:
            try:
                # Setting a fake User-Agent to prevent 403 Forbidden errors
                config = Config()
                config.browser_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
                article = Article(url, config=config)
                article.download()
                article.parse()
                
                titlu_analiza = article.title
                text_analiza = article.text
                if titlu_analiza:
                    st.success(f"Articol detectat: {titlu_analiza}")
            except Exception as e:
                st.error(f"Scraping error: {e}")

    # Manual Input: Analyzing custom text
    with input_mode[1]:
        manual_entry = st.text_area("Titlu / Paragraf:", height=100, key="manual_text_input")
        if manual_entry:
            titlu_analiza = manual_entry
    
    col_btn1, col_btn2 = st.columns([1, 5])
    with col_btn1:
        # The primary trigger for the analysis
        start_analysis = st.button("Analizează", type="primary", use_container_width=True)
    with col_btn2:
        if st.button("Reset", type="secondary"):
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- 6. ANALYSIS RESULTS ---
# Only execute if the button is pressed and there is content to analyze
if start_analysis:
    if not titlu_analiza:
        st.warning("Please provide a URL or enter text manually.")
    else:
        with st.spinner('Analyzing integrity levels...'):
            res_titlu = analyze_text(titlu_analiza)
            
            if res_titlu:
                # Main Title Verdict Card
                st.markdown(f"""
                    <div style="background: white; border: 1px solid #e2e8f0; padding: 25px; border-radius: 12px; border-top: 5px solid {res_titlu['config']['color']};">
                        <div class="verdict-badge" style="background-color: {res_titlu['config']['color']};">
                            {res_titlu['label']}
                        </div>
                        <h3 style="margin-top: 0; color: #0f172a;">{titlu_analiza}</h3>
                        <p style="color: #64748b; font-size: 15px;">{res_titlu['config']['desc']}</p>
                        <div style="display: flex; align-items: center; gap: 10px; margin-top: 20px;">
                            <span style="font-size: 13px; font-weight: 600; color: #94a3b8;">MODEL CONFIDENCE:</span>
                            <span style="font-size: 13px; font-weight: 700; color: {res_titlu['config']['color']};">{res_titlu['score']:.2%}</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                # Optional: Compare Title vs Content if URL was provided
                if text_analiza:
                    st.markdown("<br>", unsafe_allow_html=True)
                    res_content = analyze_text(text_analiza)
                    
                    st.subheader("Deep Analysis: Title vs. Content")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Verdict Titlu", res_titlu['label'])
                    with col2:
                        st.metric("Verdict Conținut", res_content['label'])
                    
                    if res_titlu['label'] != res_content['label']:
                        st.warning("Analysis complete: Discrepancy detected between title and body tone.")
                    else:
                        st.info("Analysis complete: Consistency confirmed between title and body tone.")

# --- 7. SIDEBAR LEGEND ---
with st.sidebar:
    st.title("SenticGuard v12")
    st.markdown("---")
    for cat, info in CATEGORIES.items():
        st.markdown(f"""
        <div style="margin-bottom: 15px;">
            <span style="color:{info['color']}; font-weight:bold;">{cat}</span><br>
            <small style="color:#64748b;">{info['desc']}</small>
        </div>
        """, unsafe_allow_html=True)
