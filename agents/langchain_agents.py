"""
Author : Janarddan Sarkar
file_name : langchain_agents.py 
date : 25-07-2024
description :
"""
'''
By themselves, language models can't take actions - they just output text. A big use case for LangChain is creating agents.
 Agents are systems that use LLMs as reasoning engines to determine which actions to take and the inputs to pass them.
  After executing actions, the results can be fed back into the LLM to determine whether more actions are needed, 
  or whether it is okay to finish.

In this tutorial we will build an agent that can interact with a search engine. You will be able to ask this agent questions,
 watch it call the search tool, and have conversations with it.
'''

# Import relevant functionality
# from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv(), override=True)

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
# Langmith tracking
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")


# search = TavilySearchResults(max_results=2)
# search_results = search.invoke("what is the weather in SF")
# print(search_results)
# # If we want, we can create other tools.
# # Once we have all the tools we want, we can put them in a list that we will reference later.
# tools = [search]


# # Create the agent
memory = SqliteSaver.from_conn_string(":memory:")
model = ChatOpenAI(model="gpt-4")
search = TavilySearchResults(max_results=2)
tools = [search]
agent_executor = create_react_agent(model, tools, checkpointer=memory)

# Use the agent
config = {"configurable": {"thread_id": "abc123"}}
for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content="hi im bob! and i live in sf")]}, config
):
    print(chunk)
    print("----")

for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content="whats the weather where I live?")]}, config
):
    print(chunk)
    print("----")