from langchain_groq import ChatGroq
from langchain.agents import initialize_agent, Tool
from backend.calendar_utils import create_event, check_availability
import os
from dotenv import load_dotenv

# Load environment variables 
load_dotenv()
# Initialize the Groq_key chat model
llm = ChatGroq(
    groq_api_key=os.getenv("Groq_key"),
    model_name="llama3-70b-8192",  # or llama3-70b-8192, gemma-7b-it
    temperature=0
)


tools = [
    Tool.from_function(
        name="check_availability",
        func=check_availability,
        description="Check Google Calendar availability for a specific datetime"
    ),
    Tool.from_function(
        name="create_event",
        func=create_event,
        description="Create a Google Calendar event with title, datetime, and description"
    )
]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent="chat-conversational-react-description",
    verbose=True
)

# Function to handle user input
chat_history = []

def run_agent(user_input):
    try:
        result = agent.invoke({
            "input": user_input,
            "chat_history": chat_history
        })

        # Extract only the string output
        if isinstance(result, dict) and "output" in result:
            response_text = result["output"]
        elif isinstance(result, dict) and "response" in result:
            response_text = result["response"]
        else:
            response_text = str(result)

        chat_history.append((user_input, response_text))
        return {"response": response_text}

    except Exception as e:
        print("Agent error:", e)
        return {"response": f"Error: {str(e)}"}

