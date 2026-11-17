import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
import gradio as gr

from search import load
from generate import answer

recipes, index, emb_model = load()   # load once at startup


def chat(message, history):
    message = (message or "").strip()[:300]   # cap input length
    if not message:
        return "Please type a question."
    try:
        text, sources = answer(message, recipes, index, emb_model)
    except Exception as e:
        print("Error:", e)   # shows in the Space logs
        return "Sorry, the recipe assistant is busy or unavailable right now. Please try again in a minute."
    if sources:
        links = "\n".join(
            f"- [{s['name']}]({s['url']})" + (f" by {s['author']}" if s.get("author") else "")
            for s in sources
        )
        text += f"\n\n**Sources:**\n{links}"
    return text

demo = gr.ChatInterface(
    fn=chat,
    title="DessertDex",
    description=(
        "Ask about dessert recipes. Answers come from a sample of ~3,000 recipes "
        "from the Culinary Recipes Dataset (Barba & Canals, Zenodo, ODbL)."
    ),
    examples=[
        "A chocolate and peanut butter dessert",
        "What can I make with apples and cinnamon?",
        "Something quick with bananas",
    ],
)

if __name__ == "__main__":
    demo.launch()