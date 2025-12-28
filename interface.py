import streamlit as st 
import agents 


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
        report = agents.generate_research_report_with_tools(txt)
        summary = agents.summarize_report(report)
        challenges =agents.challenges_and_futur_prediction(summary)
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

