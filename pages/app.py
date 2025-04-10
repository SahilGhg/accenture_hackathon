import streamlit as st
import re

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
    selected_sample = st.selectbox("Choose from dataset:", sample_ids)

with col2:
    st.markdown("### ✍️ Write Or Paste a Chat Below")
    chat_input = st.text_area("Paste a customer-agent conversation here:", height=300)

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
            summary = summarize_chat(chat_input)
            action = extract_action(chat_input)
            resolution = recommend_resolution(chat_input)
            team = route_ticket(chat_input)
            time = estimate_resolution_time(chat_input)

        # ===== Results Layout =====
        st.success("✅ Analysis complete!")
        st.markdown("## 🧠 AI Results Summary")
        st.markdown("---")

        with st.container():
            st.markdown(
                f"""
                <div style="padding: 1rem; background-color: #f5f0ff; border-radius: 12px; margin-bottom: 10px;">
                    <h4>📄 <span style='color:#7D3C98'>Summary</span></h4>
                    <p>{summary}</p>
                </div>
                <div style="padding: 1rem; background-color: #e0f7fa; border-radius: 12px; margin-bottom: 10px;">
                    <h4>✅ <span style='color:#00796B'>Action</span></h4>
                    <p>{action}</p>
                </div>
                <div style="padding: 1rem; background-color: #fffde7; border-radius: 12px; margin-bottom: 10px;">
                    <h4>💡 <span style='color:#F57C00'>Suggested Resolution</span></h4>
                    <p>{resolution}</p>
                </div>
                <div style="padding: 1rem; background-color: #ede7f6; border-radius: 12px; margin-bottom: 10px;">
                    <h4>🏢 <span style='color:#512DA8'>Assigned Team</span></h4>
                    <p>{team}</p>
                </div>
                <div style="padding: 1rem; background-color: #f1f8e9; border-radius: 12px;">
                    <h4>⏱️ <span style='color:#33691E'>Estimated Time</span></h4>
                    <p>{time}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
