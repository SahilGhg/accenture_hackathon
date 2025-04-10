import streamlit as st

# ✅ Must be first!
st.set_page_config(page_title="Welcome", layout="centered")

# ===== Welcome Content =====
st.markdown("<h1 style='text-align: center;'>👋 Welcome to</h1>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color:#00c4b4;'>AI Support Chat Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Streamline your customer support with smart AI agents powered by Ollama.</p>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center;'>🚀 Ready to begin?</h3>", unsafe_allow_html=True)

# ===== Centered Button (No Animation) =====
cols = st.columns([1, 2, 1])
with cols[1]:
    if st.button("👉 Go to AI Assistant", use_container_width=True):
        st.switch_page("pages/app.py")

with st.expander("📘 What does this app do?", expanded=False):
    st.markdown("""
    This tool uses multiple AI agents to:
    - 🧠 Summarize support chats
    - ✅ Extract key action items
    - 💡 Recommend resolutions
    - 🏢 Route tasks to the right teams
    - ⏱️ Estimate resolution times
    """)
