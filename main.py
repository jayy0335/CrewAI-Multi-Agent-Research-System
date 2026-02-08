"""
Main entry point for the CrewAI Multi-Agent System
"""
from src.crew import create_crew


def main():
    """Execute the CrewAI crew with the specified topic"""
    # Create the crew
    crew = create_crew()
    
    # Define the topic for research
    topic = 'latest trends in AI'
    
    # Execute the crew
    print(f"Starting CrewAI execution for topic: {topic}\n")
    print("=" * 60)
    
    result = crew.kickoff(inputs={'topic': topic})
    
    print("\n" + "=" * 60)
    print("\nFinal Result:")
    print(result)


if __name__ == "__main__":
    main()
