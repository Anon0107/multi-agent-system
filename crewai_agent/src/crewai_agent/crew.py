from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from tools.tools import web_search
import os

@CrewBase
class ResearchCrew():
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    model = LLM(
        model="anthropic/claude-haiku-4-5-20251001",
        api_key=os.getenv("ANTHROPIC_API_KEY"),  
        )
    @agent
    def researcher(self) -> Agent:
        return Agent(
            config = self.agents_config['researcher'],
            verbose = True,
            tools = [web_search],
            llm = self.model
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config = self.tasks_config['research_task'],
        )
    
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents = [
                self.researcher()
            ],
            tasks = [
                self.research_task()
            ],
            process = Process.sequential
        )
    