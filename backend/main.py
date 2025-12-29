from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
from agent.graph import app as agent_app
from langchain_core.messages import HumanMessage

app = FastAPI(title="Autonomous AI Research Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

@app.post("/research")
async def start_research(request: QueryRequest):
    inputs = {"messages": [HumanMessage(content=request.query)]}
    result = await agent_app.ainvoke(inputs)
    return {"result": result["messages"][-1].content}

@app.websocket("/ws/research")
async def websocket_research(websocket: WebSocket):
    await websocket.accept()
    
    # We will run a keepalive task in the background
    async def keepalive(ws: WebSocket):
        try:
            while True:
                await asyncio.sleep(10)
                await ws.send_json({"type": "ping"})
        except Exception:
            pass

    keepalive_task = asyncio.create_task(keepalive(websocket))
    
    try:
        data = await websocket.receive_text()
        print(f"Received query: {data}")
        inputs = {"messages": [HumanMessage(content=data)]}
        
        async for output in agent_app.astream(inputs, stream_mode="updates"):
            for node_name, state_update in output.items():
                print(f"Update from {node_name}")
                if "messages" in state_update and len(state_update["messages"]) > 0:
                    latest_message = state_update["messages"][-1]
                    
                    if hasattr(latest_message, "tool_calls") and latest_message.tool_calls:
                        tool_calls = latest_message.tool_calls
                        await websocket.send_json({"type": "tool_call", "node": node_name, "content": tool_calls})
                    else:
                        await websocket.send_json({"type": "message", "node": node_name, "content": latest_message.content})
                        
        await websocket.send_json({"type": "complete"})
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"Error: {e}")
        await websocket.send_json({"type": "error", "error": str(e)})
    finally:
        keepalive_task.cancel()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
