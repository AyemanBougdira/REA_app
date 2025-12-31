import streamlit as st
import streamlit as st 
from agents import generate_research_report_with_tools 
from agents import summarize_report 
from agents import challenges_and_futur_prediction

st.set_page_config(
    page_title="ECC Research Assistant",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# st.sidebar.header("Configuration")

# option = st.sidebar.selectbox(
#     'Select a use case:',
#     ['Research Assistant', 'Evaluator Assistant']
# )

col1, col2, col3 = st.columns([0.5, 0.4, 0.5])

with col2:
    st.image("logo.png")

st.header('REA APP: Research Expert Assistant')
# col1, col2, col3 = st.columns([1, 0.3, 1])
# with col2:
#     st.image("logo.png")




# if option == "Research":
st.markdown("### TEAM")
st.markdown("""
    - Salma BENSLIMANE: https://www.linkedin.com/in/salma-benslimane-1b3ab7246/
    - Ayeman BOUGDIRA: https://www.linkedin.com/in/abougdir/
    - Ilyas DAHAOUI: https://www.linkedin.com/in/ilyass-dahaoui/
    - Ilyasse El Khazane: https://www.linkedin.com/in/ilyasse-e-4b22871b3/
    """)

st.markdown("### About")
st.info(
    "This AI-powered research assistant helps you generate comprehensive "
    "academic reports by searching arXiv and the web. Enter a research topic "
    "to get started."
)


st.markdown("### Features")
st.markdown("""
    - 📊 Comprehensive research reports
    - 📝 Auto-generated summaries
    - 🔮 Future predictions & challenges
    - 📚 Academic citations included
    - 🌐 Web & arXiv integration
    """)
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 0.75rem;
        border: none;
        font-size: 1.1rem;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #764ba2 0%, #667eea 100%);
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .tab-content {
        padding: 1.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

txt = st.text_input("🕵🏻 Enter your research subject", "")

if st.button("Start researching"):
        report = generate_research_report_with_tools(txt)
        summary = summarize_report(report)
        challenges =challenges_and_futur_prediction(summary)
        tab1, tab2, tab3 = st.tabs([
            "✍️ Report",
            "📚 Summary",
            "🔍 Challenges & Future prediction"
        ]) 
        
        with tab1:
            st.write(report)
        with tab2:
            st.write(summary)
        with tab3:
             st.write(challenges)

