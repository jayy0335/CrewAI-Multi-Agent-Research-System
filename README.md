# CrewAI Multi-Agent Project

conda create -n crewenv python=3.11 -y

conda activate crewenv


A well-structured CrewAI multi-agent system for AI research and content creation.

## 📁 Project Structure

```
CrewAI project/
├── main.py                    # Main entry point
├── verify_structure.py        # Structure verification script
├── src/                       # Source package
│   ├── config/               # Configuration
│   │   └── settings.py       # LLM & tool settings
│   ├── agents/               # Agent definitions
│   │   ├── researcher.py
│   │   ├── content_creator.py
│   │   └── writer.py
│   ├── tasks/                # Task definitions
│   │   ├── research_task.py
│   │   ├── content_task.py
│   │   └── write_task.py
│   └── crew/                 # Crew orchestration
│       └── crew_manager.py
├── .env                      # Environment variables
└── requirements.txt          # Dependencies
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file with your API keys:

```
SERPER_API_KEY=your_serper_key_here
GROK_KEY=your_groq_key_here
```

### 3. Run the Application

```bash
python main.py
```

## 📝 Features

- **Modular Architecture**: Separate packages for agents, tasks, and configuration
- **Three Specialized Agents**:
  - **Senior Researcher**: Strategic research and task delegation
  - **Content Creator**: Engaging content creation with web search
  - **Writer**: Compelling tech storytelling
- **Sequential Task Processing**: Research → Writing → Content Creation
- **Configurable LLM**: Uses Groq's Llama 3.3 70B model
- **Web Search Integration**: SerperDev tool for real-time information

## 🔧 Customization

### Add a New Agent

Create a new file in `src/agents/`:

```python
# src/agents/your_agent.py
from crewai import Agent
from src.config import llm

your_agent = Agent(
    role='Your Role',
    goal='Your goal',
    verbose=True,
    memory=True,
    backstory="Your backstory...",
    tools=[],
    allow_delegation=False,
    llm=llm
)
```

Then update `src/agents/__init__.py` to export it.

### Add a New Task

Create a new file in `src/tasks/`:

```python
# src/tasks/your_task.py
from crewai import Task
from src.agents import your_agent

your_task = Task(
    description="Your task description with {topic} placeholder",
    expected_output="Expected output description",
    agent=your_agent,
)
```

Then update `src/tasks/__init__.py` to export it.

### Modify the Crew

Edit `src/crew/crew_manager.py` to add/remove agents and tasks.

## 📚 Documentation

- Original monolithic file preserved as `multiagents_demo.py`
- All functionality maintained in the new modular structure
- Each module is self-contained and testable

## 🎯 Benefits

- **Maintainability**: Easy to find and modify specific components
- **Scalability**: Simple to add new agents and tasks
- **Reusability**: Components can be reused across different crews
- **Testability**: Each module can be tested independently
- **Best Practices**: Follows Python package structure conventions

## 📄 License

This project uses the CrewAI framework for multi-agent orchestration.
