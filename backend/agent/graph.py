import os
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_google_genai import ChatGoogleGenerativeAI
from agent.tools import tools
from agent.state import AgentState
from dotenv import load_dotenv

load_dotenv()

# Initialize LLM with tool binding
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2,
    convert_system_message_to_human=True
)
llm_with_tools = llm.bind_tools(tools)

def call_model(state: AgentState):
    messages = state["messages"]
    system_prompt = (
        "You are an Advanced Autonomous AI Research Agent.\n"
        "Your goal is to answer the user's research queries thoroughly.\n"
        "You have tools to search the web and scrape specific URLs.\n"
        "1. Plan out what you need to search.\n"
        "2. Retrieve the search results.\n"
        "3. Scrape the URLs that look most promising.\n"
        "4. Synthesize your findings into a comprehensive, very detailed Markdown report.\n"
        "5. ALWAYS format your final answer in beautiful Markdown with headers and bullet points.\n"
        "6. Cite your sources with links."
    )
    
    messages_with_system = [{"role": "system", "content": system_prompt}] + messages
    response = llm_with_tools.invoke(messages_with_system)
    return {"messages": [response]}

workflow = StateGraph(AgentState)

workflow.add_node("agent", call_model)
workflow.add_node("action", ToolNode(tools))

workflow.set_entry_point("agent")
workflow.add_conditional_edges(
    "agent",
    tools_condition,
    {
        "tools": "action",
        END: END
    }
)
workflow.add_edge("action", "agent")

app = workflow.compile()
