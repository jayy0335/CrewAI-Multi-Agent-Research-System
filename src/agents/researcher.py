"""Senior Researcher Agent Definition"""
from crewai import Agent
from src.config import llm

# Creating a senior researcher agent with memory and verbose mode
researcher = Agent(
    role='Senior Researcher',
    goal='Oversee research operations and delegate content and writing tasks based on findings.',
    verbose=True,
    memory=True,
    backstory=(
        """ A strategic thinker at the forefront of innovation, skilled in synthesizing knowledge and "
        "delegating tasks to create impactful outputs with a high-level perspective."""
    ),
    tools=[],
    allow_delegation=False,
    llm=llm
)
