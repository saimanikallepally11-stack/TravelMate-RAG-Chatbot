import streamlit as st
from retrieval import build_or_load_collection, answer_question
from config import GOOGLE_API_KEY

st.set_page_config(page_title="TravelMate | RAG Assistant", page_icon="✈️", layout="wide")
st.markdown("""
<style>
.stApp {background: linear-gradient(135deg, #f5f8fc 0%, #eaf1f8 100%);}
.block-container {max-width: 1050px; padding-top: 2rem;}
.hero {padding: 1.6rem 1.8rem; border-radius: 18px; color: white;
background: linear-gradient(110deg,#102a43,#176b87);}
.hero h1 {margin:0; font-size:2.2rem;}
.hero p {margin:.5rem 0 0; color:#e6f4f7;}
</style>
<div class="hero">
<h1>✈️ TravelMate — AI Travel Assistant</h1>
<p>Ask questions about Telangana tourism. Answers are grounded in the documents in our knowledge base.</p>
</div>
""", unsafe_allow_html=True)

if not GOOGLE_API_KEY:
    st.error("Google API key not found. Add GOOGLE_API_KEY to your .env file.")
    st.stop()

with st.sidebar:
    st.header("About this project")
    st.write("A Retrieval-Augmented Generation (RAG) chatbot using Gemini, ChromaDB and Streamlit.")
    st.caption("Knowledge base: official Telangana tourism information.")
    if st.button("Rebuild knowledge base"):
        with st.spinner("Loading documents and creating embeddings..."):
            build_or_load_collection(force_rebuild=True)
        st.success("Knowledge base rebuilt.")

@st.cache_resource
def get_collection():
    return build_or_load_collection()

collection = get_collection()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            with st.expander("Retrieved sources"):
                for s in msg["sources"]:
                    st.write(f"- {s}")

question = st.chat_input("Ask about places, heritage, attractions or travel in Telangana...")
if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)
    with st.chat_message("assistant"):
        with st.spinner("Searching tourism documents and preparing an answer..."):
            result = answer_question(collection, question)
        st.markdown(result["answer"])
        if result["sources"]:
            with st.expander("Retrieved sources"):
                for s in result["sources"]:
                    st.write(f"- {s}")
    st.session_state.messages.append({
        "role": "assistant", "content": result["answer"], "sources": result["sources"]
    })
