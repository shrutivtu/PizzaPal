# 🍕 PizzaPal - AI Pizza Ordering Assistant

A fun and interactive pizza ordering chatbot built with Gradio and OpenAI's GPT-3.5-turbo. PizzaPal guides customers through the pizza ordering process with personality, humor, and pizza puns while collecting structured order data.

## ✨ Features

- **Interactive Chat Interface**: Friendly conversational AI that makes ordering pizza enjoyable
- **Step-by-Step Ordering**: Guides users through pizza selection, toppings, extras, dietary notes, and delivery address
- **JSON Output**: Automatically structures complete orders into clean JSON format
- **Pizza Personality**: Uses emojis, puns, and chef-like enthusiasm to enhance the user experience
- **Real-time Processing**: Powered by OpenAI's GPT-3.5-turbo for natural language understanding

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- OpenAI API key
- Required Python packages (see Installation)

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
```env
OPENAI_API_KEY=your_openai_api_key_here
```

4. Run the application:
```bash
python app.py
```

5. Open your browser to the provided Gradio URL (typically `http://localhost:7860`)

## 🍕 How It Works

### Menu Items
The bot offers selections from a predefined menu:
- **Pizzas**: Margherita, Pepperoni, Vegan Delight
- **Toppings**: Olives, Mushrooms, Onions, Extra Cheese
- **Extras**: Coke, Garlic Bread

### Ordering Process
1. **Pizza Selection**: Choose from available pizza types
2. **Toppings**: Select desired toppings
3. **Extras**: Add drinks or sides
4. **Dietary Notes**: Specify any dietary requirements (vegan, halal, allergies)
5. **Delivery Address**: Provide delivery location

### Output Format
Once the order is complete, PizzaPal outputs a structured JSON object:
```json
{
    "pizza": "Margherita",
    "toppings": ["Olives", "Extra Cheese"],
    "extras": ["Coke"],
    "dietary_notes": "No allergies",
    "address": "123 Main St, City, State"
}
```

## 🛠️ Technical Details

### Key Components

- **Gradio Interface**: Provides the web-based chat interface
- **OpenAI Integration**: Uses GPT-3.5-turbo for natural language processing
- **JSON Extraction**: Regex-based parsing to extract structured order data
- **Chat History**: Maintains conversation context throughout the ordering process

### Configuration

The system prompt can be customized to:
- Modify the bot's personality
- Update menu items
- Change the ordering workflow
- Adjust output format

## 🎨 Customization

### Adding Menu Items
Update the `menu` dictionary to add new pizzas, toppings, or extras:
```python
menu = {
    "pizzas": ["Margherita", "Pepperoni", "Vegan Delight", "BBQ Chicken"],
    "toppings": ["Olives", "Mushrooms", "Onions", "Extra Cheese", "Peppers"],
    "extras": ["Coke", "Garlic Bread", "Wings"]
}
```

### Modifying Personality
Adjust the `system_prompt` to change PizzaPal's personality, tone, or behavior patterns.

### UI Customization
Modify the Gradio interface elements to change labels, styling, or layout.

## 🔧 Functions

### `chat_with_agent(user_text)`
Main chat processing function that handles user input and generates responses.

### `extract_json(text)`
Parses assistant responses to extract JSON order data using regex patterns.

### `reset_chat()`
Resets the conversation history and order state for new sessions.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## 🆘 Support

For issues or questions:
- Check the console output for debugging information
- Ensure your OpenAI API key is valid and has sufficient credits
- Verify all dependencies are installed correctly

## 🎉 Enjoy Your Pizza!

PizzaPal makes ordering pizza fun and efficient. Whether you're building a restaurant ordering system or just want to see AI in action, this project demonstrates how to create engaging conversational interfaces with structured data output.
