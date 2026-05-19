from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.project.wrappers import TaskMethod
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

    @agent
    def analyst(self) -> Agent:
        return Agent(
            config = self.agents_config['analyst'],
            verbose = True,
            llm = self.model
        )
    
    @agent
    def writer(self) -> Agent:
        return Agent(
            config = self.agents_config['writer'],
            verbose = True,
            llm = self.model
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config = self.tasks_config['research_task'],
        )
    
    @task
    def analyst_task(self) -> Task:
        return Task(
            config = self.tasks_config['analyst_task']
        )
    
    @task
    def write_task(self) -> Task:
        return Task(
            config = self.tasks_config['write_task']
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents = [
                self.researcher(),
                self.analyst(),
                self.writer()
            ],
            tasks = [
                self.research_task(),
                self.analyst_task(),
                self.write_task()
            ],
            process = Process.sequential
        )
    