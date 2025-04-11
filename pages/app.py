import streamlit as st
import re
import sqlite3
import pandas as pd

# ===== Page Setup =====
st.set_page_config(page_title="AI Assistant", layout="wide", initial_sidebar_state="collapsed")

# ===== Optional CSS to remove any unwanted form borders =====
st.markdown("""
    <style>
    section.main > div:has(> form) {
        border: none !important;
        box-shadow: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# ===== Import AI Agents =====
from agents.summarizer_agent import summarize_chat
from agents.action_extractor_agent import extract_action
from agents.resolution_agent import recommend_resolution
from agents.router_agent import route_ticket
from agents.time_estimator_agent import estimate_resolution_time
from agents.predict_category_agent import predict_category

# ===== Load Sample Dataset =====
def load_sample_chats():
    with open("data/sample_chats.txt", "r", encoding="utf-8") as file:
        raw_data = file.read().strip()

    conversations = re.split(r"\n-{3,}\n", raw_data)
    chat_list = []

    for conv in conversations:
        conv = conv.strip()
        if conv:
            match = re.search(r"^(.*?)\nConversation ID:\s*(TECH_\d+)", conv, re.DOTALL)
            if match:
                title = match.group(1).strip()
                convo_id = match.group(2).strip()
                display_id = f"{convo_id} - {title}"
            else:
                display_id = f"Chat {len(chat_list)+1}"
            chat_list.append({"id": display_id, "chat": conv})

    return chat_list

# ===== Load Chats =====
sample_chats = load_sample_chats()
sample_ids = ["None"] + [chat["id"] for chat in sample_chats]

# ===== Header =====
st.markdown("<h1 style='text-align: center; color:#7D3C98;'>🤖 AI Support Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Analyze customer support chats with multi-agent intelligence powered by Ollama.</p>", unsafe_allow_html=True)
st.markdown("---")


# ===== Input Section =====
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### 📁Select a Sample Chat")
    selected_sample = st.selectbox("Choose from dataset:", sample_ids, key="selected_sample")
 
    if "chat_input" not in st.session_state:
        st.session_state.chat_input = ""
    
    # Load selected sample into session_state
    if selected_sample != "None":
        for chat in sample_chats:
            if chat["id"] == selected_sample:
                if st.session_state.chat_input != chat["chat"]:
                    st.session_state.chat_input = chat["chat"]
                break
    else:
        st.session_state.chat_input = ""

with col2:
    st.markdown("### ✍️ Write Or Paste a Chat Below")
    chat_input = st.text_area("Paste a customer-agent conversation here:", value=st.session_state.chat_input, key="chat_input_area", height=300)

# Load chat from sample if selected
if selected_sample != "None" and not chat_input.strip():
    for chat in sample_chats:
        if chat["id"] == selected_sample:
            chat_input = chat["chat"]
            break

# ===== Analyze Form =====
with st.form("analyze_form"):
    st.markdown("<h3 style='text-align:center;'>🔍 Run AI Analysis</h3>", unsafe_allow_html=True)
    col_center = st.columns([1, 2, 1])
    with col_center[1]:
        submitted = st.form_submit_button("Analyze Chat", use_container_width=True)

# 🔧 Add spacing to prevent ghost border after button
st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

# ===== Run Agent Analysis and Display Results =====
if submitted:
    if not chat_input.strip():
        st.warning("⚠️ Please paste a chat or select one from the dataset.")
    else:
        with st.spinner("Running multi-agent analysis..."):
            results = {}
            
            status_placeholders = {
                "summary": st.empty(),
                "action": st.empty(),
                "resolution": st.empty(),
                "team": st.empty(),
                "time": st.empty(),
                "category": st.empty()
            }

            try:
                with st.spinner("Running summarizer..."):
                    results["summary"] = summarize_chat(chat_input)
                    status_placeholders["summary"].success("✅ Summary generated successfully!")
            except Exception as e:
                results["summary"] = f"❌ Error generating summary: {e}"

            try:
                with st.spinner("Extracting actions..."):
                    results["action"] = extract_action(chat_input)
                    status_placeholders["action"].success("✅ Actions extracted successfully!")
            except Exception as e:
                results["action"] = f"❌ Error extracting actions: {e}"

            try:
                with st.spinner("Recommending resolution..."):
                    resolution, source, keywords = recommend_resolution(chat_input)
                    results["resolution"] = resolution
                    results["source"] = source           
                    results["keywords"] = keywords

                    status_placeholders["resolution"].success("✅ Resolution suggested!")
            except Exception as e:
                results["resolution"] = f"❌ Error recommending resolution: {e}"
                results["source"] = "N/A"
                results["keywords"] = []


            try:
                with st.spinner("Routing to appropriate team..."):
                    results["team"] = route_ticket(chat_input)
                    status_placeholders["team"].success("✅ Ticket routed!")
            except Exception as e:
                results["team"] = f"❌ Error routing ticket: {e}"

            try:
                with st.spinner("Estimating resolution time..."):
                    results["time"] = estimate_resolution_time(chat_input)
                    status_placeholders["time"].success("✅ Time estimated!")
            except Exception as e:
                results["time"] = f"❌ Error estimating time: {e}"

            try:
                with st.spinner("Predicting category..."):
                    results["category"] = predict_category(chat_input)
                    status_placeholders["category"].success("📂 Category predicted successfully!")
            except Exception as e:
                results["category"] = f"❌ Error predicting category: {e}"

            for placeholder in status_placeholders.values():
                placeholder.empty()

        st.markdown("---")
        # ===== Results Layout =====
        st.success("✅ Analysis complete!")
        st.markdown("## 🧠 AI Results Summary")
       
        
        keywords = results.get('keywords', [])
        if isinstance(keywords, str):
            keywords = [keywords]

        with st.container():
            st.markdown(f"""
                <div style="padding: 1rem; background-color: #f5f0ff; border-radius: 12px; margin-bottom: 10px;">
                    <h4>📄 <span style='color:#7D3C98'>Summary</span></h4>
                    <p>{results['summary']}</p>
                </div>

                <div style="padding: 1rem; background-color: #e0f7fa; border-radius: 12px; margin-bottom: 10px;">
                    <h4>✅ <span style='color:#00796B'>Action</span></h4>
                    <p>{results['action']}</p>
                </div>

                <div style="padding: 1rem; background-color: #fffde7; border-radius: 12px; margin-bottom: 10px;">
                    <h4>💡 <span style='color:#F57C00'>Suggested Resolution</span></h4>
                    <p><strong>{results['resolution']}</strong></p>
                <p style='margin-top: 6px; color: #777;'>📚 <i>Source: {results['source']}</i></p>

                <hr style="margin: 10px 0;">
                <p style='margin-top: 10px; color: #616161;'>
                🔑 <strong>Keywords extracted:</strong> {", ".join(keywords)}
                    </p>
                </div>

                <div style="padding: 1rem; background-color: #fce4ec; border-radius: 12px; margin-bottom: 10px;">
                    <h4>📂 <span style='color:#C2185B'>Predicted Category</span></h4>
                    <p>{results['category']}</p>
                </div>

                <div style="padding: 1rem; background-color: #ede7f6; border-radius: 12px; margin-bottom: 10px;">
                    <h4>🏢 <span style='color:#512DA8'>Assigned Team</span></h4>
                    <p>{results['team']}</p>
                </div>

                <div style="padding: 1rem; background-color: #f1f8e9; border-radius: 12px;">
                    <h4>⏱️ <span style='color:#33691E'>Estimated Time</span></h4>
                    <p>{results['time']}</p>
                </div>
            """, unsafe_allow_html=True)

# ===== Download Analysis Report =====
st.markdown("---")
if "results" in locals() and results:
    report_lines = [
        "📄 AI Support Chat Analysis Report",
        "----------------------------------",
        f"Summary:\n{results.get('summary', '')}",
        "\n\nActions:\n" + results.get("action", ""),
        "\n\nSuggested Resolution:\n" + results.get("resolution", ""),
        "\n\nAssigned Team:\n" + results.get("team", ""),
        "\n\nEstimated Time:\n" + results.get("time", ""),
        "\n\nPredicted Category:\n" + results.get("category", ""),
        "\n\nKeywords Extracted:\n" + ", ".join(results.get("keywords", []))
    ]
    report_text = "\n".join(report_lines)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.download_button(
            label="📥 Download Analysis Report",
            data=report_text,
            file_name="chat_analysis_report.txt",
            mime="text/plain"
        )

# ===== Feedback Section =====
st.markdown("---")
st.markdown("## ⭐️ Share Your Feedback")

rating = st.slider("Rate the AI assistant’s suggestions:", 1, 5, 3)
comments = st.text_area("Additional Comments (optional):")

if st.button("Submit Feedback"):
    try:
        conn = sqlite3.connect("data/tickets.db")
        cursor = conn.cursor()
        convo_id = selected_sample if selected_sample != "None" else "Custom Input"
        cursor.execute("INSERT INTO feedback (conversation_id, rating, comments) VALUES (?, ?, ?)",
                       (convo_id, rating, comments))
        conn.commit()
        conn.close()
        st.success("✅ Thank you! Your feedback has been recorded.")
    except Exception as e:
        st.error(f"❌ Error saving feedback: {e}")

with st.expander("📋 View Submitted Feedback", expanded=False):
    df_feedback = None
    try:
        conn = sqlite3.connect("data/tickets.db")
        df_feedback = pd.read_sql_query("SELECT * FROM feedback ORDER BY id DESC", conn)
        conn.close()
        if df_feedback.empty:
            st.info("No feedback submitted yet.")                 
        else:
            st.dataframe(df_feedback, use_container_width=True)
    except Exception as e:
        st.error(f"❌ Error loading feedback: {e}")
    
    if df_feedback is not None and not df_feedback.empty:
        if st.button("🗑️ Clear All Feedback"):
            try:
                conn = sqlite3.connect("data/tickets.db")
                cursor = conn.cursor()
                cursor.execute("DELETE FROM feedback")
                conn.commit()
                conn.close()
                st.success("✅ All feedback entries cleared!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error clearing feedback: {e}")
