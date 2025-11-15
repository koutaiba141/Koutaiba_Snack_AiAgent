# Koutaiba Snack AI Agent

This project is an AI-powered agent that uses a local Llama3 model and a FastAPI backend to interact with a Supabase database.

## Architecture

The project is composed of the following components:

*   **FastAPI Backend:** A Python web framework for building APIs. The backend provides endpoints for interacting with the AI agent and the database.
*   **Supabase:** A backend-as-a-service platform that provides a PostgreSQL database, authentication, and other services.
*   **Llama3:** A large language model that is used to power the AI agent.
*   **OpenRouter:** A service that provides access to a variety of large language models.

## Workflow

1.  The user interacts with the AI agent through a frontend (not included in this project).
2.  The frontend sends requests to the FastAPI backend.
3.  The FastAPI backend uses the Llama3 model via OpenRouter to process the user's request.
4.  The backend interacts with the Supabase database to store and retrieve data.
5.  The backend returns a response to the frontend.

## Technologies Used

*   [FastAPI](https://fastapi.tiangolo.com/)
*   [Supabase](https://supabase.io/)
*   [Llama3](https://ai.meta.com/blog/meta-llama-3/)
*   [OpenRouter](https://openrouter.ai/)
*   [Python](https://www.python.org/)

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    ```
2.  **Create a virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```
3.  **Install the dependencies:**
    ```bash
    pip install -r requirments.txt
    ```
4.  **Create a `.env` file:**
    Create a `.env` file in the root of the project and add the following environment variables:
    ```
    SUPABASE_URL=<your-supabase-url>
    SUPABASE_KEY=<your-supabase-key>
    OPENROUTER_API_KEY=<your-openrouter-api-key>
    ```
5.  **Run the application:**
    ```bash
    uvicorn api.main:app --reload
    ```
