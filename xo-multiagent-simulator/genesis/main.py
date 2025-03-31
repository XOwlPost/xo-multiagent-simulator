from fastapi import FastAPI, Request
import uvicorn

app = FastAPI()

@app.post("/dispatch")
async def dispatch_task(req: Request):
    data = await req.json()
    agent = data.get("agent")
    task = data.get("task")

    if agent == "AppAgent":
        return {"agent": agent, "response": await appagent_logic(task)}
    elif agent == "VaultBot":
        return {"agent": agent, "response": await vaultbot_logic(task)}
    else:
        return {"error": "Unknown agent", "agent": agent}

async def appagent_logic(task):
    return {"message": f"AppAgent handled task: {task}"}

async def vaultbot_logic(task):
    return {"message": f"VaultBot secured task: {task}"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
