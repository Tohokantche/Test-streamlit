import streamlit as st
from main import ResearchCrew  # Import the ResearchCrew class from main.py
import os
import pandas as pd
import time 

st.title('Your Research Assistant')
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
os.environ["SERPER_API_KEY"] = st.secrets["SERPER_API_KEY"]


# 1. Initialize session state
if 'button_disabled' not in st.session_state:
    st.session_state.button_disabled = False

if 'completed_task' not in st.session_state:
    st.session_state.completed_task = False

# 2. Define a callback function to run when the button is clicked
def disable_button():
    if not topic or not detailed_questions:
        st.error("Please fill all the fields.")
    if st.session_state.completed_task:
        st.error("Task already completed !")
    
def get_cost(crew):
    costs = 0.150 * (crew.usage_metrics.prompt_tokens + crew.usage_metrics.completion_tokens) / 1_000_000
    # Convert UsageMetrics instance to a DataFrame
    usage_cp = crew.usage_metrics.dict().copy()
    usage_cp.update({"Total costs": f"${costs:.4f}"})
    df_usage_metrics = pd.DataFrame([usage_cp])
    return df_usage_metrics

def on_text_change():
    st.session_state.completed_task = False
    
with st.sidebar:
    st.header('Enter Research Details')
    topic = st.text_input("Main topic of your research:",on_change=on_text_change)
    detailed_questions = st.text_area("Specific questions or subtopics you are interested in exploring:", on_change=on_text_change)

if st.button('Run Research', on_click=disable_button, disabled=st.session_state.button_disabled):
    if topic and detailed_questions and not st.session_state.completed_task:
        with st.spinner("Wait for a moment ...", show_time=True):
            inputs = f"Research Topic: {topic}\nDetailed Questions: {detailed_questions}"
            research_crew = ResearchCrew(inputs)
            st.divider()
            st.subheader("Results of your research project:")
            # crew, result = research_crew.run()
            # st.divider()
            # st.subheader("Detailed cost of the agent run:")
            # st.dataframe(get_cost(crew))
            # st.divider()
            # st.subheader("Results of your research project:")
            # st.markdown(result.raw)
            time.sleep(5)
            st.success("Done!")
            st.session_state.completed_task = True
            
        
