# src/tools/search.py
from uagents import Agent, Context, Model
from tavily import TavilyClient
import os

class Request(Model):
    message: str

class Response(Model):
    response: str

# Initialize Tavily Search uAgent
tavily_agent = Agent(
    name="Tavily Search Tool",
    port=8002,  # Different port from your main agent
    seed="TAVILY_TOOL_SEED",
    endpoint=["http://localhost:8002/submit"]
)

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tavily_agent.on_event("startup")
async def startup_handler(ctx: Context):
    ctx.logger.info(f"Tavily Search Tool started at address: {tavily_agent.address}")

@tavily_agent.on_message(model=Request)
async def handle_search(ctx: Context, sender: str, msg: Request):
    try:
        result = tavily_client.search(msg.message)
        await ctx.send(sender, Response(response=str(result)))
    except Exception as e:
        await ctx.send(sender, Response(response=f"Error: {str(e)}"))

if __name__ == "__main__":
    tavily_agent.run()