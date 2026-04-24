import streamlit as st
from openai import OpenAI
from database import init_db, save_entry, load_history

# 1. Setup & Configuration
st.set_page_config(page_title="ImpactLog AI", page_icon="📈")
db_conn = init_db()

# Secret Key Handling (For GitHub/Streamlit Cloud)
# On your local PC, it looks for st.secrets or an environment variable
api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")

st.title("🚀 Worklog to Performance Summary")
st.markdown("---")

# 2. Input Section
input_text = st.text_area("What did you work on today?", placeholder="e.g., Fixed the login timeout bug and updated the client docs.")

# 3. Execution Logic
if st.button("Generate Professional Summary"):
    if not api_key:
        st.error("Please provide an API Key to proceed.")
    elif not input_text:
        st.warning("Please enter your work logs.")
    else:
        with st.spinner("AI is quantifying your impact..."):
            try:
                client = OpenAI(api_key=api_key)
                
                # The "STAR" Prompt Engineering
                prompt = f"""
                Convert these messy work logs into a professional performance summary:
                LOGS: {input_text}
                
                Provide:
                1. Weekly Summary (Executive style)
                2. Self-Appraisal Points (Use STAR: Situation, Task, Action, Result)
                3. LinkedIn Achievement Post
                """
                
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}]
                )
                
                summary = response.choices[0].message.content
                
                # Save to local database (Offline Feature)
                save_entry(db_conn, input_text)
                
                # Display Results
                st.success("Analysis Complete!")
                st.markdown(summary)
                
                st.download_button("Download Report", summary, file_name="Performance_Review.md")
                
            except Exception as e:
                st.error(f"Error: {e}")

# 4. History Section
st.sidebar.header("History (Offline Storage)")
history_df = load_history(db_conn)
st.sidebar.dataframe(history_df)
