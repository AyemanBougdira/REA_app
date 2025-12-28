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

# st.header('Automating Research using AI')

# if option == "Research":
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

