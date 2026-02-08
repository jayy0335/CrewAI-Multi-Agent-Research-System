"""Content Creator Task Definition"""
from crewai import Task
from src.agents import content_creator

content_creator_task = Task(
    description=(
        "Conduct an in-depth analysis to identify the next significant trend in {topic}. "
        "Evaluate the trend's strengths and weaknesses, and craft a compelling narrative that contextualizes its relevance. "
        "Your deliverable should present clear, actionable insights, highlight market opportunities, and outline any potential risks. "
        "Ensure the content is engaging, strategically structured, and suitable for a professional audience."
    ),
    expected_output=(
        "A well-structured, three-paragraph report that summarizes the trend, its advantages and challenges, "
        "and its implications for the market and audience engagement."
    ),
    agent=content_creator,
)
