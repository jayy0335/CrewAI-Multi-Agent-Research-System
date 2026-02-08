"""Research Task Definition"""
from crewai import Task
from src.agents import researcher

research_task = Task(
    description=(
        "Conduct a comprehensive investigation into the topic: {topic}. "
        "Analyze key developments, insights, and data to form a strategic overview. "
        "Based on your findings, define clear directives for the Content Creator and Writer agents—"
        "assigning relevant tasks that align with the content strategy and communication goals. "
        "Ensure your instructions include context, priorities, and expected outcomes for each agent."
    ),
    expected_output=(
        "A strategic research summary accompanied by two well-defined delegated task briefs: "
        "one for content creation and one for writing, each tailored to their respective agents."
    ),
    agent=researcher,
)
