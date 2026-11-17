import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
import gradio as gr

from search import load
from generate import answer

recipes, index, emb_model = load()   # load once at startup


def chat(message, history):
    text, sources = answer(message, recipes, index, emb_model)
    if sources:
        links = "\n".join(f"- [{s['name']}]({s['url']})" for s in sources)
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