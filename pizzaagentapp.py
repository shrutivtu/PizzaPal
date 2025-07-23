import gradio as gr
from openai import OpenAI
import json
from dotenv import load_dotenv
import os
import re

# Load API key from .env
load_dotenv()
client = OpenAI()  

# Detailed pizza menu with prices
menu = {
    "pizzas": [
        { "name": "Margherita", "description": "Tomato sauce, mozzarella, basil", "price_eur": 7.5 },
        { "name": "Pepperoni", "description": "Tomato sauce, mozzarella, spicy pepperoni", "price_eur": 9.0 },
        { "name": "Quattro Formaggi", "description": "Mozzarella, gorgonzola, parmesan, emmental", "price_eur": 10.0 },
        { "name": "Prosciutto e Funghi", "description": "Ham, mushrooms, mozzarella, tomato sauce", "price_eur": 9.5 },
        { "name": "Diavola", "description": "Spicy salami, chili, onions", "price_eur": 9.8 },
        { "name": "Vegetariana", "description": "Bell peppers, mushrooms, onions, olives", "price_eur": 8.9 },
        { "name": "Capricciosa", "description": "Ham, mushrooms, artichokes, olives", "price_eur": 10.5 },
        { "name": "BBQ Chicken", "description": "Chicken, BBQ sauce, red onion, mozzarella", "price_eur": 10.2 },
        { "name": "Tuna & Onion", "description": "Tuna, red onion, mozzarella", "price_eur": 9.0 },
        { "name": "Hawaiian", "description": "Ham, pineapple, mozzarella", "price_eur": 9.2 }
    ],
    "extra_toppings": [
        { "name": "Extra mozzarella", "price_eur": 1.0 },
        { "name": "Mushrooms", "price_eur": 0.8 },
        { "name": "Jalapeños", "price_eur": 0.7 },
        { "name": "Olives", "price_eur": 0.8 },
        { "name": "Pineapple", "price_eur": 0.8 },
        { "name": "Pepperoni", "price_eur": 1.2 },
        { "name": "Ham", "price_eur": 1.2 },
        { "name": "Artichokes", "price_eur": 1.0 },
        { "name": "Gorgonzola", "price_eur": 1.3 },
        { "name": "Vegan cheese", "price_eur": 1.5 }
    ],
    "sides": [
        { "name": "Garlic Bread", "price_eur": 3.5 },
        { "name": "Cheesy Garlic Bread", "price_eur": 4.5 },
        { "name": "Chicken Wings (6 pcs)", "price_eur": 5.0 },
        { "name": "Mixed Salad", "price_eur": 4.0 },
        { "name": "Fries", "price_eur": 3.0 },
        { "name": "Dips (BBQ, garlic, etc.)", "price_eur": 0.5 }
    ],
    "drinks": [
        { "name": "Coca-Cola", "size": "0.5L", "price_eur": 2.0 },
        { "name": "Fanta", "size": "0.5L", "price_eur": 2.0 },
        { "name": "Sprite", "size": "0.5L", "price_eur": 2.0 },
        { "name": "Mineral Water", "size": "0.5L", "price_eur": 1.5 },
        { "name": "Iced Tea (peach/lemon)", "size": "0.5L", "price_eur": 2.2 },
        { "name": "Beer (local)", "size": "0.33L", "price_eur": 2.5 }
    ]
}

# Updated system prompt
system_prompt = f"""
You're PizzaPal 🍕 — the friendliest, funniest, most flavorful pizza-ordering assistant ever created!

Your job is to help the user place a delicious pizza order, but with style and sass. Speak like a happy chef excited to serve. Use emojis, make pizza puns, and sprinkle in some personality, but **always collect the order data step-by-step**.

🎯 Our complete menu with prices in EUR:

**PIZZAS:**
{json.dumps(menu['pizzas'], indent=2)}

**EXTRA TOPPINGS:**
{json.dumps(menu['extra_toppings'], indent=2)}

**SIDES:**
{json.dumps(menu['sides'], indent=2)}

**DRINKS:**
{json.dumps(menu['drinks'], indent=2)}

🍕 Here's the ordering process:
1. Ask what pizza they'd like from our pizza menu (show prices and descriptions!)
2. Ask if they want any extra toppings (show prices for each)
3. Ask about sides and drinks (show all options with prices)
4. Ask about any dietary notes (vegan, halal, allergies, etc.)
5. Get their delivery address
6. Ask for payment method (ONLY accept "cash on delivery" or "card" - no other methods!)
7. Calculate and show the total price before finalizing

🍕 Once everything is collected, respond ONLY with a JSON object like this:

{{
    "pizza": {{"name": "...", "price": 0.0}},
    "extra_toppings": [{{"name": "...", "price": 0.0}}],
    "sides": [{{"name": "...", "price": 0.0}}],
    "drinks": [{{"name": "...", "size": "...", "price": 0.0}}],
    "dietary_notes": "...",
    "address": "...",
    "payment_method": "cash on delivery" or "card",
    "total_price_eur": 0.0
}}

⚠️ VERY IMPORTANT:
- Always show prices when presenting options!
- Calculate the total price accurately
- Be chatty and fun throughout the ordering process!
- But once the order is complete, stop joking and ONLY output the JSON with no extra text.
"""

# Global variables to track state
chat_history = []
order_complete = False
final_order_json = None

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

def format_order_summary(order_json):
    """Format the order JSON into a human-readable summary"""
    summary = "🎉 **Order Complete!** Here's your delicious order summary:\n\n"
    
    # Pizza section
    pizza = order_json.get('pizza', {})
    if pizza:
        summary += f"🍕 **Pizza:** {pizza.get('name', 'N/A')} - €{pizza.get('price', 0):.2f}\n"
    
    # Extra toppings
    extra_toppings = order_json.get('extra_toppings', [])
    if extra_toppings:
        summary += "\n🧄 **Extra Toppings:**\n"
        for topping in extra_toppings:
            summary += f"   • {topping.get('name', 'N/A')} - €{topping.get('price', 0):.2f}\n"
    
    # Sides
    sides = order_json.get('sides', [])
    if sides:
        summary += "\n🍞 **Sides:**\n"
        for side in sides:
            summary += f"   • {side.get('name', 'N/A')} - €{side.get('price', 0):.2f}\n"
    
    # Drinks
    drinks = order_json.get('drinks', [])
    if drinks:
        summary += "\n🥤 **Drinks:**\n"
        for drink in drinks:
            size_info = f" ({drink.get('size', '')})" if drink.get('size') else ""
            summary += f"   • {drink.get('name', 'N/A')}{size_info} - €{drink.get('price', 0):.2f}\n"
    
    # Dietary notes
    dietary_notes = order_json.get('dietary_notes', '')
    if dietary_notes and dietary_notes.strip():
        summary += f"\n📝 **Dietary Notes:** {dietary_notes}\n"
    
    # Address
    address = order_json.get('address', '')
    if address and address.strip():
        summary += f"\n📍 **Delivery Address:** {address}\n"
    
    # Payment method
    payment_method = order_json.get('payment_method', '')
    if payment_method and payment_method.strip():
        payment_emoji = "💳" if payment_method.lower() == "card" else "💵"
        summary += f"\n{payment_emoji} **Payment Method:** {payment_method.title()}\n"
    
    # Total
    total = order_json.get('total_price_eur', 0)
    summary += f"\n💰 **Total: €{total:.2f}**\n"
    
    summary += "\nYour amazing pizza is being prepared! 🔥 Check the 'Final Order' tab for the technical details."
    
    return summary

def transcribe_audio(audio):
    """Transcribe audio using OpenAI Whisper API"""
    if audio is None:
        return ""
    
    try:
        # Open the audio file and transcribe
        with open(audio, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        return transcript.text
    except Exception as e:
        print(f"Transcription error: {e}")
        return f"Sorry, I couldn't understand your voice message. Error: {str(e)}. Please try again or type your message."

def chat_with_pizzapal(message, history):
    global chat_history, order_complete, final_order_json
    
    # Build the conversation history for OpenAI
    messages = [{"role": "system", "content": system_prompt}]
    
    # Add all previous messages from history
    for human_msg, assistant_msg in history:
        messages.append({"role": "user", "content": human_msg})
        if assistant_msg:  # Check if assistant replied
            messages.append({"role": "assistant", "content": assistant_msg})
    
    # Add the current message
    messages.append({"role": "user", "content": message})
    
    try:
        # Get response from OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        
        reply = response.choices[0].message.content
        
        # Check if this contains a final order JSON
        json_str = extract_json(reply)
        if json_str:
            try:
                order_json = json.loads(json_str)
                order_complete = True
                final_order_json = order_json
                
                # Add a nice completion message after the JSON
                reply += "\n\n🎉 **Order Complete!** Your delicious pizza is being prepared! Check the 'Final Order' tab to see your order details."
                
            except Exception as e:
                print("JSON parsing error:", e)
        
        return reply
    
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return f"Sorry, I'm having trouble connecting to my pizza brain right now. Error: {str(e)}. Please try again!"

def handle_voice_message(audio, history):
    """Process recorded voice message"""
    if audio is None:
        return history, "", gr.update(visible=False), get_final_order()
    
    # Transcribe the audio
    transcribed_text = transcribe_audio(audio)
    
    if transcribed_text and transcribed_text.strip() and not transcribed_text.startswith("Sorry, I couldn't"):
        # Process the transcribed text through the chat system
        bot_response = chat_with_pizzapal(transcribed_text, history)
        history.append((f"🎤 {transcribed_text}", bot_response))
    elif transcribed_text.startswith("Sorry, I couldn't"):
        # Handle transcription error
        history.append((f"🎤 [Voice input error]", transcribed_text))
    
    return history, "", gr.update(visible=False), get_final_order()

def get_final_order():
    """Return the final order JSON formatted nicely"""
    if final_order_json:
        return json.dumps(final_order_json, indent=2)
    else:
        return "No order completed yet. Keep chatting with PizzaPal to place your order!"

def reset_conversation():
    """Reset the conversation and order state"""
    global chat_history, order_complete, final_order_json
    chat_history = []
    order_complete = False
    final_order_json = None
    return [], "", get_final_order()

# Custom CSS for better styling
css = """
.gradio-container {
    max-width: 900px;
    margin: 0 auto;
}

.chat-message {
    padding: 10px;
    margin: 5px 0;
    border-radius: 10px;
}

#final-order {
    background-color: #f0f0f0;
    padding: 15px;
    border-radius: 10px;
    font-family: monospace;
}

.voice-section {
    background-color: #f8f9fa;
    padding: 15px;
    border-radius: 10px;
    margin: 10px 0;
}

.compact-input {
    display: flex;
    align-items: center;
    gap: 8px;
}

.voice-btn {
    min-width: 45px !important;
    height: 45px !important;
    border-radius: 8px !important;
    font-size: 18px !important;
}

/* Align button heights with textbox */
button {
    height: 42px !important;
    min-height: 42px !important;
}

.textbox input {
    height: 42px !important;
}
"""

# Create the interface
with gr.Blocks(css=css, title="🍕 PizzaPal - AI Pizza Ordering Assistant") as demo:
    gr.Markdown("""
    # 🍕 PizzaPal - AI Pizza Ordering Assistant
    
    Welcome to PizzaPal! I'm your friendly AI assistant ready to help you order the perfect pizza. 
    You can **type** your messages or use the **🎤 Audio** input below to speak!
    """)
    
    with gr.Tab("💬 Chat with PizzaPal"):
        chatbot = gr.Chatbot(
            height=400,
            placeholder="Start chatting with PizzaPal! Try saying 'Hi' or 'I want to order a pizza'",
            show_copy_button=True
        )
        
        # Text input
        with gr.Row():
            msg = gr.Textbox(
                placeholder="Type your message here...",
                show_label=False,
                scale=4
            )
            submit_btn = gr.Button("Send 🍕", scale=1, variant="primary")
            clear_btn = gr.Button("🔄 Reset", scale=1, variant="secondary")
        
        # Voice input section
        gr.Markdown("### 🎤 Voice Input")
        with gr.Row():
            audio_input = gr.Audio(
                sources=["microphone"],
                type="filepath",
                label="Record your voice message",
                scale=3
            )
            voice_submit_btn = gr.Button("Send Voice Message 🎤", scale=1, variant="secondary")
    
    with gr.Tab("🧾 Final Order"):
        order_display = gr.Textbox(
            label="Your Pizza Order (JSON)",
            value="No order completed yet. Keep chatting with PizzaPal to place your order!",
            lines=15,
            max_lines=20,
            elem_id="final-order"
        )
        refresh_order_btn = gr.Button("Refresh Order 🔄", variant="secondary")
    
    with gr.Tab("ℹ️ How to Use"):
        gr.Markdown("""
        ## How to Use PizzaPal Voice Chat
        
        ### 🎤 Voice Input
        1. Scroll to the **Voice Input** section below the text input
        2. Click on the microphone area to start recording
        3. Allow microphone access when prompted by your browser
        4. Speak clearly into your microphone
        5. When done recording, click **"Send Voice Message 🎤"**
        6. Your speech will be transcribed and processed automatically
        
        ### ⌨️ Text Input
        - Type messages in the text box and click "Send 🍕"
        - Both voice and text inputs work the same way!
        
        ### 🍕 Ordering Process
        PizzaPal will guide you through:
        1. **Pizza Selection** - Choose from our extensive menu with prices
        2. **Extra Toppings** - Add delicious toppings (each priced individually)
        3. **Sides & Drinks** - Garlic bread, wings, salads, and beverages
        4. **Dietary Notes** - Any special requirements
        5. **Address** - Where to deliver your pizza
        6. **Payment Method** - Cash on delivery or card only
        7. **Price Calculation** - See your total before confirming
        
        ### 🧾 Final Order
        - Once complete, your order will appear in the "Final Order" tab
        - The order is saved as JSON format for easy processing
        
        ### Tips for Voice Input
        - Speak clearly and at a normal pace
        - Try to minimize background noise
        - If transcription seems wrong, you can always retype your message
        - Make sure your browser has microphone permissions enabled
        """)
    
    # Event handlers
    def submit_message(message, history):
        if message.strip():
            bot_response = chat_with_pizzapal(message, history)
            history.append((message, bot_response))
            return history, "", get_final_order()
        return history, message, get_final_order()
    
    def clear_chat():
        return reset_conversation()
    
    # Connect the events
    submit_btn.click(
        submit_message, 
        inputs=[msg, chatbot], 
        outputs=[chatbot, msg, order_display]
    )
    
    msg.submit(
        submit_message, 
        inputs=[msg, chatbot], 
        outputs=[chatbot, msg, order_display]
    )
    
    voice_submit_btn.click(
        handle_voice_message,
        inputs=[audio_input, chatbot],
        outputs=[chatbot, msg, audio_input, order_display]
    )
    
    clear_btn.click(
        clear_chat,
        outputs=[chatbot, msg, order_display]
    )
    
    refresh_order_btn.click(
        get_final_order,
        outputs=order_display
    )

if __name__ == "__main__":
    demo.launch()