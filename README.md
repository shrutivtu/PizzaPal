# 🍕 PizzaPal - AI Pizza Ordering Assistant

A fun and interactive pizza ordering chatbot built with Gradio and OpenAI's GPT-3.5-turbo. PizzaPal guides customers through the pizza ordering process with personality, humor, and pizza puns while collecting structured order data. Now featuring **voice input support** with Whisper transcription!

## ✨ Features

* **Interactive Chat Interface**: Friendly conversational AI that makes ordering pizza enjoyable
* **🎤 Voice Input Support**: Speak your order using OpenAI's Whisper transcription
* **Comprehensive Menu**: Detailed pizza menu with prices in EUR, including pizzas, toppings, sides, and drinks
* **Step-by-Step Ordering**: Guides users through pizza selection, toppings, extras, dietary notes, delivery address, and payment method
* **Order Confirmation**: Built-in confirmation step before finalizing orders
* **Structured Output**: Automatically formats complete orders into clean JSON with human-readable summary
* **Pizza Personality**: Uses emojis, puns, and chef-like enthusiasm to enhance the user experience
* **Real-time Processing**: Powered by OpenAI's GPT-3.5-turbo for natural language understanding
* **Payment Processing**: Supports cash on delivery and card payments

## 🚀 Quick Start

### Prerequisites

* Python 3.7+
* OpenAI API key
* Required Python packages (see Installation)

### Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd pizzapal
```

2. Install required dependencies:
```bash
pip install gradio openai python-dotenv
```

3. Create a `.env` file in the project root:
```
OPENAI_API_KEY=your_openai_api_key_here
```

4. Run the application:
```bash
python app.py
```

5. Open your browser to the provided Gradio URL (typically `http://localhost:7860`)

## 🍕 How It Works

### Menu Items

The bot offers selections from a comprehensive menu with EUR pricing:

**Pizzas** (€7.50 - €10.50):
* Margherita, Pepperoni, Quattro Formaggi, Prosciutto e Funghi
* Diavola, Vegetariana, Capricciosa, BBQ Chicken
* Tuna & Onion, Hawaiian

**Extra Toppings** (€0.70 - €1.50):
* Extra mozzarella, Mushrooms, Jalapeños, Olives, Pineapple
* Pepperoni, Ham, Artichokes, Gorgonzola, Vegan cheese

**Sides** (€0.50 - €5.00):
* Garlic Bread, Cheesy Garlic Bread, Chicken Wings
* Mixed Salad, Fries, Various Dips

**Drinks** (€1.50 - €2.50):
* Coca-Cola, Fanta, Sprite, Mineral Water
* Iced Tea, Local Beer

### Ordering Process

1. **Pizza Selection**: Choose from 10 available pizza types with descriptions and prices
2. **Extra Toppings**: Select desired additional toppings with individual pricing
3. **Sides & Drinks**: Add garlic bread, wings, salads, and beverages
4. **Dietary Notes**: Specify any dietary requirements (vegan, halal, allergies)
5. **Delivery Address**: Provide complete delivery location
6. **Payment Method**: Choose between "cash on delivery" or "card"
7. **Price Calculation**: See itemized pricing and total cost
8. **Order Confirmation**: Final review before order completion

### Voice Input

* **🎤 Record Messages**: Click the microphone to record voice messages
* **Automatic Transcription**: Uses OpenAI Whisper for accurate speech-to-text
* **Seamless Integration**: Voice messages processed just like text input
* **Error Handling**: Graceful handling of transcription errors

## 📋 Output Format

Once the order is complete, PizzaPal outputs both:

1. **Human-readable summary** with emojis and formatting
2. **Structured JSON object**:

```json
{
    "pizza": {"name": "Margherita", "price": 7.5},
    "extra_toppings": [
        {"name": "Extra mozzarella", "price": 1.0},
        {"name": "Mushrooms", "price": 0.8}
    ],
    "sides": [
        {"name": "Garlic Bread", "price": 3.5}
    ],
    "drinks": [
        {"name": "Coca-Cola", "size": "0.5L", "price": 2.0}
    ],
    "dietary_notes": "No allergies",
    "address": "123 Main St, City, State",
    "payment_method": "card",
    "total_price_eur": 14.8
}
```

## 🛠️ Technical Details

### Key Components

* **Gradio Interface**: Provides web-based chat interface with voice input support
* **OpenAI Integration**: 
  - GPT-3.5-turbo for natural language processing
  - Whisper for voice transcription
* **JSON Extraction**: Regex-based parsing to extract structured order data
* **Chat History**: Maintains conversation context throughout the ordering process
* **Order State Management**: Global order tracking and status updates
* **Audio Processing**: File-based audio handling for voice messages

### Key Functions

* `chat_with_pizzapal(message, history)`: Main chat processing function
* `transcribe_audio(audio)`: Handles voice message transcription using Whisper
* `extract_json(text)`: Parses assistant responses for JSON order data
* `format_order_summary(order_json)`: Creates human-readable order summaries
* `submit_message()` & `handle_voice_message()`: Input processing functions
* `reset_conversation()`: Resets chat and order state

### Configuration

The system prompt includes:
* Complete menu with pricing in EUR
* Step-by-step ordering workflow
* Personality guidelines with emojis and puns
* JSON output format specification
* Payment method restrictions
* Order confirmation requirements

## 🎨 Customization

### Adding Menu Items

Update the `menu` dictionary to add new items with prices:

```python
menu = {
    "pizzas": [
        {"name": "Custom Pizza", "description": "Your creation", "price_eur": 12.0}
    ],
    "extra_toppings": [
        {"name": "Truffle", "price_eur": 2.5}
    ],
    "sides": [
        {"name": "Mozzarella Sticks", "price_eur": 4.5}
    ],
    "drinks": [
        {"name": "Fresh Juice", "size": "0.3L", "price_eur": 3.0}
    ]
}
```

### Modifying Personality

Adjust the `system_prompt` to change PizzaPal's personality, tone, or behavior patterns.

### UI Customization

* Modify CSS for styling changes
* Update Gradio components for different layouts
* Customize tab structure and organization

## 🎤 Voice Features

### Browser Requirements
* Modern browser with microphone support
* HTTPS connection (for production deployments)
* Microphone permissions enabled

### Audio Quality Tips
* Speak clearly and at normal pace
* Minimize background noise
* Ensure stable internet connection
* Allow microphone access when prompted

### Troubleshooting Voice Input
* Check browser console for audio errors
* Verify microphone permissions
* Test with different browsers if issues persist
* Fall back to text input if voice fails

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly (including voice features)
5. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## 🆘 Support

For issues or questions:
* Check the console output for debugging information
* Ensure your OpenAI API key is valid and has sufficient credits
* Verify all dependencies are installed correctly
* Test microphone permissions for voice features
* Check network connectivity for API calls

## 🎉 Enjoy Your Pizza!

PizzaPal makes ordering pizza fun and efficient with both text and voice interactions. Whether you're building a restaurant ordering system or exploring conversational AI, this project demonstrates how to create engaging interfaces with structured data output and multimodal input support.
