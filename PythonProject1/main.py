"""
Main entry point for Koutaiba Snack AI Agent
Run this file to start interacting with the agent via command line
"""
from agent import create_agent
import sys


def print_separator():
    """Print a visual separator"""
    print("\n" + "=" * 60 + "\n")


def main():
    """Main function to run the interactive chat"""
    print("🍕 Welcome to Koutaiba Snack AI Call Center 🍕")
    print_separator()
    print("Initializing AI agent... Please wait...")

    try:
        # Create the agent
        agent = create_agent()
        print("✅ Agent initialized successfully!")
        print("\nYou can now chat with the AI assistant.")
        print("Type 'quit', 'exit', or 'bye' to end the conversation.")
        print("Type 'reset' to clear conversation history.")
        print_separator()

        # Main conversation loop
        while True:
            try:
                # Get user input
                user_input = input("Customer: ").strip()

                # Check for exit commands
                if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                    print("\n🙏 Thank you for contacting Koutaiba Snack! Goodbye!")
                    break

                # Check for reset command
                if user_input.lower() == 'reset':
                    agent.reset_memory()
                    print("\n🔄 Conversation history cleared!\n")
                    continue

                # Skip empty inputs
                if not user_input:
                    continue

                # Get agent response
                print("\nAgent: ", end="", flush=True)
                response = agent.chat(user_input)
                print(response)
                print_separator()

            except KeyboardInterrupt:
                print("\n\n⚠️  Interrupted by user. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")
                print("Let's try again...\n")

    except Exception as e:
        print(f"\n❌ Failed to initialize agent: {str(e)}")
        print("\nPlease make sure:")
        print("1. Ollama is running: ollama serve")
        print("2. The model is installed: ollama pull llama3.1:8b-instruct-q4_K_M")
        print("3. Your restaurant API is running at http://127.0.0.1:8000")
        sys.exit(1)


if __name__ == "__main__":
    main()