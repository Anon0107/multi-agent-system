from crew import ResearchCrew

def run():
    topic = input("Enter a topic: ")
    result = ResearchCrew().crew().kickoff(inputs= {"topic": topic})
    print(result)

if __name__ == "__main__":
    run()