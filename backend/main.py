from fastapi import FastAPI, Request
from backend.agent import run_agent
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
@app.post("/chat")
@app.post("/")
async def chat(payload: dict):
    user_message = payload.get("message")
    if not user_message:
        return {"response": "Please provide a message."}
    return run_agent(user_message)
