"""Write Task Definition"""
from crewai import Task
from src.agents import writer
from .research_task import research_task

write_task = Task(
    description=(
        "Compose an insightful article on {topic}. "
        "Focus on the latest trends and how it's impacting the industry. "
        "This article should be easy to understand, engaging, and positive."
    ),
    expected_output="A 4 paragraph article on given advancements formatted as markdown.",
    agent=writer,
    async_execution=False,
)

# Set task context
write_task.context = [research_task]
