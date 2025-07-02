from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from calendar_utils import create_event, check_availability
from dotenv import load_dotenv
import os

# Load environment variables 
load_dotenv()

# Initialize the OpenAI chat model
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)


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
def run_agent(user_input):
    return agent.run(user_input)
