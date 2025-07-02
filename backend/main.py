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
async def chat_endpoint(request: Request):
    data = await request.json()
    user_input = data.get("message", "")
    print("👉 User input:", user_input)

    try:
        response = run_agent(user_input)
    except Exception as e:
        response = str(e)
    return {"response": response}

