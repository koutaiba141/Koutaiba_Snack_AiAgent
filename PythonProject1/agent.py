"""
Main Agent Logic for Koutaiba Snack AI Assistant
"""
from langchain.agents import AgentExecutor, create_react_agent
from langchain.memory import ConversationBufferMemory
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from tools import tools
from prompts import SYSTEM_PROMPT

class KoutaibaSnackAgent:
    def __init__(self, model_name: str = "llama3.1:8b-instruct-q4_K_M"):
        """
        Initialize the Koutaiba Snack AI Agent

        Args:
            model_name: Name of the Ollama model to use
        """
        # Initialize the local LLM
        self.llm = OllamaLLM(
            model=model_name,
            temperature=0.7,  # Balance between creative and focused
            num_ctx=4096,     # Context window size
        )

        # Initialize memory for conversation history
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="output"
        )

        # Create the proper ReAct prompt template with all required variables
        react_prompt = PromptTemplate.from_template(
            """{system_prompt}

TOOLS:
------
You have access to the following tools:

{tools}

TOOL NAMES: {tool_names}

FORMAT:
-------
To use a tool, please use the following format:

```
Thought: Do I need to use a tool? Yes
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
```

When you have a response to say to the Human, or if you do not need to use a tool, you MUST use the format:

```
Thought: Do I need to use a tool? No
Final Answer: [your response here]
```

CONVERSATION HISTORY:
{chat_history}

Begin!

Question: {input}
{agent_scratchpad}"""
        )

        # Prepare the prompt with system instructions
        self.prompt = react_prompt.partial(system_prompt=SYSTEM_PROMPT)

        # Create the ReAct agent
        self.agent = create_react_agent(
            llm=self.llm,
            tools=tools,
            prompt=self.prompt
        )

        # Create the agent executor with memory
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=tools,
            memory=self.memory,
            verbose=True,  # Set to False in production
            handle_parsing_errors=True,
            max_iterations=10,  # Prevent infinite loops
            return_intermediate_steps=False
        )

    def chat(self, user_input: str) -> str:
        """
        Process user input and return agent response

        Args:
            user_input: The customer's message

        Returns:
            The agent's response
        """
        try:
            response = self.agent_executor.invoke({"input": user_input})
            return response["output"]
        except Exception as e:
            error_msg = str(e)
            print(f"\n⚠️  Debug - Error details: {error_msg}\n")
            return f"I apologize, but I encountered an error processing your request. Could you please rephrase that?"

    def reset_memory(self):
        """Clear conversation history"""
        self.memory.clear()

    def get_conversation_history(self) -> list:
        """Get the current conversation history"""
        return self.memory.buffer_as_messages

def create_agent(model_name: str = "llama3.1:8b-instruct-q4_K_M") -> KoutaibaSnackAgent:
    """
    Factory function to create a new agent instance

    Args:
        model_name: Name of the Ollama model to use

    Returns:
        Initialized KoutaibaSnackAgent
    """
    return KoutaibaSnackAgent(model_name=model_name)