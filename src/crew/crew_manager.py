"""Crew Manager - Orchestrates agents and tasks"""
from crewai import Crew, Process
from src.agents import researcher, writer, content_creator
from src.tasks import research_task, write_task, content_creator_task


def create_crew():
    """
    Create and configure the CrewAI crew with agents and tasks.
    
    Returns:
        Crew: Configured crew ready for execution
    """
    # Forming the tech-focused crew with enhanced configurations
    crew = Crew(
        agents=[researcher, writer, content_creator],
        tasks=[research_task, write_task, content_creator_task],
        process=Process.sequential  # Sequential task execution
    )
    
    return crew
