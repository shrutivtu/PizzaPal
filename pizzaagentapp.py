import gradio as gr
from openai import OpenAI
import json
from dotenv import load_dotenv
import os
import re

# Load API key from .env
load_dotenv()
client = OpenAI()  

# Sample pizza menu
menu = {
    "pizzas": ["Margherita", "Pepperoni", "Vegan Delight", "BBQ Chicken", "Four Cheese", "Spicy Veggie", "Hawaiian", "Meat Feast", "Buffalo Chicken", "Pesto Veggie", "Four Seasons"],
    "toppings": ["Olives", "Mushrooms", "Onions", "Extra Cheese", "Jalapenos", "Spinach", "Pineapple", "Basil", "Garlic", "Bell Peppers"],
    "extras": ["Coke", "Garlic Bread", "Water", "Iced Tea", "Salad", "Brownie", "Cheesy Sticks", "Wings", "Fries", "Sparkling Water"]
}

# Updated system prompt
system_prompt = f"""
You're PizzaPal 🍕 — the friendliest, funniest, most flavorful pizza-ordering assistant ever created!

Your job is to help the user place a delicious pizza order, but with style and sass. Speak like a happy chef excited to serve. Use emojis, make pizza puns, and sprinkle in some personality, but **always collect the order data step-by-step**.

🎯 Here's the plan:
1. Ask what pizza they'd like from this menu: {menu['pizzas']}. Give them the full menu options in order to choose.
2. Offer tasty toppings from this list: {menu['toppings']}. Give them the full menu toppings options in order to choose.
3. Suggest extras like drinks or sides: {menu['extras']}. Give them the full menu extras in order to choose.
4. Ask about any dietary notes (vegan, halal, allergies).
5. Get their delivery address. You must NOT finalize the order unless you have a full address


🍕 Once everything is collected, respond ONLY with a JSON object like this:

{{
    "pizza": "...",
    "toppings": ["...", "..."],
    "extras": ["..."],
    "dietary_notes": "...",
    "address": "..."
}}

⚠️ VERY IMPORTANT:
- After the first message, show all the menu options.
- Be chatty and fun throughout the ordering process!
- But once the order is complete, stop joking and ONLY output the JSON with no extra text.
- ONLY accept orders for items on the menu. If a user requests something not listed, politely inform them it's not available and suggest alternatives.
"""

# Dialog history
chat_history = []
order_complete = False

# Helper to extract JSON from assistant reply
def extract_json(text):
    pattern = r"```(?:json)?(.*?)```|({.*?})"
    matches = re.findall(pattern, text, re.DOTALL)
    for g1, g2 in matches:
        for g in (g1, g2):
            g = g.strip()
            if g.startswith("{") and g.endswith("}"):
                return g
    # fallback if assistant replies with raw JSON without wrapping
    if text.strip().startswith("{") and text.strip().endswith("}"):
        return text.strip()
    return None

# Chat function
def chat_with_agent(user_text):
    global chat_history, order_complete
    chat_history.append({"role": "user", "content": user_text})
    messages = [{"role": "system", "content": system_prompt}] + chat_history

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    reply = response.choices[0].message.content
    chat_history.append({"role": "assistant", "content": reply})

    # Debug print - optional
    print("Assistant reply:", reply)

    order_json = None
    json_str = extract_json(reply)
    if json_str:
        try:
            order_json = json.loads(json_str)
            order_complete = True
        except Exception as e:
            print("JSON parsing error:", e)
            order_json = None

    return reply, json.dumps(order_json, indent=2) if order_complete else ""

# Reset function
def reset_chat():
    global chat_history, order_complete
    chat_history = []
    order_complete = False
    return "", ""

# Gradio interface
interface = gr.Interface(
    fn=chat_with_agent,
    inputs=gr.Textbox(label="💬 Type your message to the Pizza Agent"),
    outputs=[
        gr.Textbox(label="🤖 Agent Reply"),
        gr.Textbox(label="🧾 Final Order (JSON)")
    ],
    live=False,
    allow_flagging="never",
    title="🍕 PizzaPal - AI Pizza Agent"
)

interface.launch()