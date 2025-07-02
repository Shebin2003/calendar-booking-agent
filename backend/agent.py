from langchain_groq import ChatGroq
from langchain.agents import initialize_agent, Tool
from backend.calendar_utils import create_event, check_availability
import os
from dotenv import load_dotenv
from langchain.schema import HumanMessage, AIMessage

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
    global chat_history
    try:
        agent_response = agent.invoke({
            "input": user_input,
            "chat_history": chat_history
        })
        chat_history.append(("user", user_input))
        chat_history.append(("ai", agent_response["output"]))  # or agent_response.get("output")

        return {"response": agent_response["output"]}
    except Exception as e:
        print("Agent error:", e)
        return {"response": f"Error: {str(e)}"}

