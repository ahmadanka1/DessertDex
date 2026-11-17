import os
import sys

import streamlit as st

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

# Streamlit Cloud keeps secrets in st.secrets; copy them into the environment
# so generate.py can read them with os.environ.
for key in ("GEMINI_API_KEY", "GEMINI_MODEL"):
    if key not in os.environ:
        try:
            os.environ[key] = st.secrets[key]
        except Exception:
            pass

from search import load      # noqa: E402
from generate import answer  # noqa: E402

MAX_QUESTIONS_PER_SESSION = 20
MAX_QUESTION_CHARS = 300

st.set_page_config(page_title="DessertDex", page_icon="🍰")


@st.cache_resource
def get_resources():
    return load()   # recipes, index, embedding model: loaded once, shared across users


recipes, index, emb_model = get_resources()

st.title("🍰 DessertDex")
st.caption(
    "Ask about dessert recipes. Answers come from a sample of 3,000 recipes in the "
    "Culinary Recipes Dataset (Barba & Canals, Zenodo, ODbL). Always check the linked "
    "original recipe."
)

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.count = 0

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if not st.session_state.messages:
    st.write("Try: *a chocolate and peanut butter dessert*, *apples and cinnamon*, *something quick with bananas*")

question = st.chat_input("Ask for a dessert...")

if question:
    question = question.strip()[:MAX_QUESTION_CHARS]
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        if st.session_state.count >= MAX_QUESTIONS_PER_SESSION:
            reply = "You've reached the question limit for this session. Please come back later."
        else:
            with st.spinner("Searching recipes..."):
                try:
                    text, sources = answer(question, recipes, index, emb_model)
                    st.session_state.count += 1
                    if sources:
                        links = "\n".join(
                            f"- [{s['name']}]({s['url']})"
                            + (f" by {s['author']}" if s.get("author") else "")
                            for s in sources
                        )
                        text += f"\n\n**Sources:**\n{links}"
                    reply = text
                except Exception as e:
                    print("Error:", e)   # visible in the app logs
                    reply = "Sorry, the recipe assistant is busy or unavailable right now. Please try again in a minute."
        st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})