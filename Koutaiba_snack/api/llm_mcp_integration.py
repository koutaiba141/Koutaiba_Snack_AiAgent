import os
from dotenv import load_dotenv
from openai import OpenAI
from api.mcp_server import mcp  # import the running MCP instance directly

# Load API key
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise ValueError("Please set OPENROUTER_API_KEY in your .env file")

# ------------------ LLM Client ------------------ #
llm_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

# ------------------ System Prompt ------------------ #
SYSTEM_PROMPT = """
You are a restaurant assistant for 'Koutaiba Snack'. You have the following tools:

1. get_menu() - full menu
2. get_categories() - menu categories
3. get_items_by_category(category)
4. get_item_details(item_name)
5. get_available_items()
6. create_order(customer_name, customer_phone, items, table_number=None, notes=None)
7. get_order_details(order_id)
8. get_customer_orders(customer_name)
9. get_ingredient_details(ingredient_id)
10. get_item_ingredients(item_id)

Rules:
- Use these tools to fetch real restaurant data.
- If the user wants to order, ask for name, phone, items, table number, notes.
IMPORTANT:

- When the user asks for real restaurant data, respond ONLY with the function call that should be executed.
- Do NOT answer directly; instead, output the exact tool call with parameters.

Examples:

User: "Show me the full menu"
Assistant: "get_menu()"

User: "I want details for pizza"
Assistant: "get_item_details('pizza')"

User: "I want to order a pizza"
Assistant: "create_order(customer_name='John Doe', customer_phone='1234567890', items=['pizza'], table_number=5, notes=None)"

"""

# ------------------ Function to Ask LLM ------------------ #
def ask_llm(user_messages):
    """
    user_messages: list of dicts like [{"role": "user", "content": "..."}]
    """
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + user_messages

    response = llm_client.chat.completions.create(
        model="qwen/qwen3-235b-a22b:free",
        messages=messages,
        extra_headers={
            "HTTP-Referer": "http://localhost",
            "X-Title": "Koutaiba Snack Chatbot",
        },
        extra_body={},
    )

    llm_text = response.choices[0].message.content

    # ------------------ Call MCP tools ------------------ #
    # If LLM returns text like "get_menu()", execute it
    try:
        if "(" in llm_text and ")" in llm_text:
            result = mcp.call(llm_text.strip())
            return result
    except Exception as e:
        return {"error": f"LLM or MCP call failed: {str(e)}"}

    return {"response": llm_text}

# ------------------ Example Usage ------------------ #
if __name__ == "__main__":
    print("🤖 LLM + MCP Integration Running!")

    conversation_history = [
        #{"role": "user", "content": "Show me the full menu"},
        #{"role": "user", "content": "I want to order a pizza"}
    ]

    result = ask_llm(conversation_history)
    print(result)
