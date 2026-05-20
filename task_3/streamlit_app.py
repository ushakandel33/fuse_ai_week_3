import streamlit as st
import pandas as pd
import json
from executor import run_pipeline

st.set_page_config(page_title="Text-to-SQL Pipeline", layout="wide")

st.title("🤖 Text-to-SQL Pipeline Chat")
st.markdown("Ask natural language questions to query the PostgreSQL database. Uses Gemini Prompt Chaining.")

question = st.text_input("Enter your natural language query:", placeholder="e.g. List all products")

if st.button("Generate & Execute"):
    if question:
        with st.spinner("Executing Prompt Chain (Decompose ➔ Generate ➔ Execute ➔ Evaluate)..."):
            response = run_pipeline(question)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("1. Decomposition (LLM Call 1)")
                if response["decomposition"]:
                    try:
                        # Try to parse it to show pretty JSON format
                        st.json(json.loads(response["decomposition"]))
                    except:
                        st.code(response["decomposition"])
                else:
                    st.error("Failed to decompose.")
                    
                st.subheader("2. Final SQL (LLM Call 2 / Call 3)")
                st.code(response["sql"], language="sql")
                
                if response["retry_needed"]:
                    st.warning("⚠️ Initial execution threw an error. LLM Call 3 successfully triggered a self-correction rewrite.")
            
            with col2:
                st.subheader("3. Execution Status")
                if response["status"] == "success":
                    st.success(f"Execution Successful! Retrieved {len(response['result'])} rows.")
                    st.dataframe(pd.DataFrame(response["result"]))
                else:
                    st.error(f"Execution Failed: {response['error']}")
    else:
        st.warning("Please enter a question.")