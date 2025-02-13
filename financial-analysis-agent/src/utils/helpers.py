from typing import Any, Callable, List, Optional, TypedDict, Union, Annotated
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI

def agent_node(state, agent, name):
    """Helper function to create agent nodes."""
    # Add information needed to the state if available
    if "information_needed" in state:
        message_content = f"""Information needed:
        {', '.join(state['information_needed'])}
        
        Query: {state['messages'][-1].content}"""
        state['messages'][-1] = HumanMessage(content=message_content)

    result = agent.invoke(state)
    return {"messages": [HumanMessage(content=result["output"], name=name)]}


def create_agent(
    llm: ChatOpenAI,
    tools: list,
    system_prompt: str,
) -> AgentExecutor:
    """Create a function-calling agent and add it to the graph."""
    system_prompt += (
        "\nWork autonomously according to your specialty, using the tools available to you."
        " Do not ask for clarification."
        " Your other team members (and other teams) will collaborate with you with their own specialties."
        " You are chosen for a reason! You are one of the following team members: {team_members}."
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    agent = create_openai_functions_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools)
    return executor

def create_team_supervisor(llm: ChatOpenAI, system_prompt, members) -> Callable:
    """Create an LLM-based router with enhanced reasoning."""
    options = ["FINISH"] + members
    function_def = {
        "name": "route",
        "description": "Select the next role based on query analysis.",
        "parameters": {
            "title": "routeSchema",
            "type": "object",
            "properties": {
                "next": {
                    "title": "Next",
                    "anyOf": [
                        {"enum": options},
                    ],
                },
                "reasoning": {
                    "title": "Reasoning",
                    "type": "string",
                    "description": "Explanation for why this agent should act next"
                },
                "information_needed": {
                    "title": "Information Needed",
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of specific information needed from this agent"
                }
            },
            "required": ["next", "reasoning", "information_needed"],
        },
    }

    enhanced_system_prompt = system_prompt + """
    Think step by step:
    1. What specific financial information is needed to fully answer the query?
    2. Which agent is best suited to find each piece of information?
    3. What order of operations would give the most comprehensive answer?
    4. Have we gathered all necessary information to FINISH?

    For SEC Analyst:
    - Use for historical financial data, regulatory filings, official numbers
    - Best for detailed financial metrics, risk factors, and regulatory information
    
    For Search:
    - Use for current market context, recent developments, analyst opinions
    - Best for industry trends, competitor analysis, and real-time updates

    Only FINISH when you have:
    1. Gathered all necessary information from both sources if needed
    2. Confirmed the response addresses the original query comprehensively
    3. Validated that no additional context is needed
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", enhanced_system_prompt),
        MessagesPlaceholder(variable_name="messages"),
        (
            "system",
            """Given the conversation above, who should act next? Think carefully about:
            1. What information do we have so far?
            2. What's still missing to provide a complete answer?
            3. Which agent can best provide the missing information?
            
            Select one of: {options}""",
        ),
    ]).partial(options=str(options), team_members=", ".join(members))

    return (
        prompt
        | llm.bind_functions(functions=[function_def], function_call="route")
        | JsonOutputFunctionsParser()
    )