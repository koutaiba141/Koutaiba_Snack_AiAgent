# AI_Agent - Koutaiba Snack Restaurant AI Call Center

A complete AI-powered restaurant management system featuring an intelligent call center agent that handles customer inquiries and orders using local LLM models. The project consists of two main components: a FastAPI backend with database integration and an AI agent interface.

## 🌟 Features

- **Intelligent Conversational AI**: Natural language interaction for menu browsing and order placement
- **Local LLM**: Runs on Ollama (Llama 3.1) for privacy and offline capabilities
- **RESTful API**: FastAPI backend with comprehensive restaurant management endpoints
- **Database Integration**: Supabase PostgreSQL for data persistence
- **Stock Management**: Real-time inventory tracking and availability checks
- **Order Processing**: Complete order lifecycle from creation to tracking
- **Multi-Model Support**: Integration with OpenRouter for alternative LLM options
- **MCP Integration**: Model Context Protocol server for advanced integrations

## 📁 Project Structure

```
AI_Agent/
├── Koutaiba_snack/          # Backend API and services
│   ├── api/                 # FastAPI application
│   │   ├── controllers/     # API route handlers
│   │   ├── database/        # Database connection and queries
│   │   ├── models/          # Pydantic models
│   │   ├── services/        # Business logic
│   │   ├── utils/           # Utility functions
│   │   ├── main.py          # FastAPI entry point
│   │   └── mcp_server.py    # MCP server implementation
│   ├── .env                 # Environment variables (not tracked)
│   └── requirments.txt      # Python dependencies
│
└── PythonProject1/          # AI Agent Interface
    ├── agent.py             # LangChain agent implementation
    ├── tools.py             # LangChain tools for API integration
    ├── prompts.py           # System prompts and templates
    ├── main.py              # CLI interface
    ├── utils.py             # Helper functions
    └── requirements.txt     # Python dependencies
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+**
- **Ollama** (for local LLM)
- **Supabase Account** (for database)
- **OpenRouter API Key** (optional, for cloud LLM access)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AI_Agent
   ```

2. **Set up the Backend (Koutaiba_snack)**
   ```bash
   cd Koutaiba_snack
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirments.txt
   ```

3. **Configure Environment Variables**
   
   Create `.env` file in `Koutaiba_snack/`:
   ```env
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_key
   OPENROUTER_API_KEY=your_openrouter_api_key
   ```

4. **Start the Backend API**
   ```bash
   uvicorn api.main:app --reload
   ```
   The API will be available at `http://127.0.0.1:8000`

5. **Set up the AI Agent (PythonProject1)**
   
   Open a new terminal:
   ```bash
   cd PythonProject1
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

6. **Install and Start Ollama**
   ```bash
   # Install Ollama from https://ollama.ai
   ollama serve
   
   # Pull the required model
   ollama pull llama3.1:8b-instruct-q4_K_M
   ```

7. **Run the AI Agent**
   ```bash
   python main.py
   ```

## 💡 Usage

### Using the AI Call Center Agent

Once the agent is running, you can interact naturally:

```
Customer: What's on the menu?
Agent: We have a delicious selection! Our menu includes...

Customer: I'd like to order 2 cheeseburgers and a large pizza
Agent: Let me search for those items for you...

Customer: What ingredients are in the margherita pizza?
Agent: [Provides detailed ingredient list]
```

**Available Commands:**
- `quit`, `exit`, `bye` - End the conversation
- `reset` - Clear conversation history

### API Endpoints

The FastAPI backend provides comprehensive endpoints:

**Menu Management**
- `GET /menu` - Get complete menu
- `GET /menu/categories` - List all categories
- `GET /menu/categories/{category}` - Get items by category
- `GET /menu/items/{item_id}` - Get item details
- `GET /menu/search?q={query}` - Search menu items
- `GET /menu/available` - Get available items

**Stock Management**
- `GET /stock/check-item/{item_id}?quantity={qty}` - Check stock availability

**Ingredients**
- `GET /ingredients/items/{item_id}` - Get item ingredients

**Orders**
- `POST /orders` - Create new order
- `GET /orders/customer/{name}` - Get customer order history

Visit `http://127.0.0.1:8000/docs` for interactive API documentation.

## 🏗️ Architecture

### Backend (Koutaiba_snack)
- **Framework**: FastAPI for high-performance async API
- **Database**: Supabase (PostgreSQL) for data persistence
- **LLM Integration**: OpenRouter for cloud-based LLM access
- **MCP Server**: Model Context Protocol for advanced integrations

### AI Agent (PythonProject1)
- **Framework**: LangChain for agent orchestration
- **LLM**: Ollama (Llama 3.1) running locally
- **Agent Type**: ReAct (Reasoning and Acting) agent
- **Memory**: Conversation buffer for context retention
- **Tools**: Custom tools for API integration

### Data Flow

```
User Input → AI Agent → LangChain Tools → FastAPI Backend → Supabase Database
                ↓                              ↓
            Local LLM                    Business Logic
         (Llama 3.1)                  (Stock, Orders, Menu)
```

## 🛠️ Technologies

**Backend**
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [Supabase](https://supabase.io/) - Open source Firebase alternative
- [Pydantic](https://pydantic-docs.helpmanual.io/) - Data validation
- [asyncpg](https://github.com/MagicStack/asyncpg) - PostgreSQL driver

**AI Agent**
- [LangChain](https://python.langchain.com/) - LLM orchestration
- [Ollama](https://ollama.ai/) - Local LLM runtime
- [Llama 3.1](https://ai.meta.com/llama/) - Meta's language model

**Optional**
- [OpenRouter](https://openrouter.ai/) - Multi-model LLM API

## 📝 Development

### Running Tests

Backend tests:
```bash
cd Koutaiba_snack
python api/test_api.py
python api/test_all_apis.py
```

### Project Configuration

Both projects include:
- `.gitignore` - Excludes virtual environments, cache, and secrets
- `.idea/` - PyCharm/IntelliJ configuration
- `.venv/` - Python virtual environment

## 🔒 Security Notes

**⚠️ IMPORTANT**: Never commit the `.env` file or expose API keys.

The `.env` file contains sensitive credentials:
- Supabase URL and API keys
- OpenRouter API keys
- Database passwords

Ensure `.env` is listed in `.gitignore` before committing.

## 🐛 Troubleshooting

**Agent fails to start:**
- Ensure Ollama is running: `ollama serve`
- Verify model is installed: `ollama list`
- Check backend API is running at `http://127.0.0.1:8000`

**API errors:**
- Verify `.env` file has correct credentials
- Check Supabase connection
- Review logs for detailed error messages

**Stock check failures:**
- Ensure database has stock/ingredients data
- Verify item_id exists in menu

## 📄 License

This project is provided as-is for educational and commercial purposes.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📧 Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Built with ❤️ for Koutaiba Snack Restaurant**
