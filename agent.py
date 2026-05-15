import anthropic
from dotenv import load_dotenv
from tavily import TavilyClient
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio
import os

load_dotenv()
client = anthropic.Anthropic()

async def mcp_server(tool_name:str, tool_input:str):
    server_params = StdioServerParameters(
        command = r"C:\Users\liowk\Documents\mcp server\venv\Scripts\python",
        args = ["server.py"],
        cwd = r"C:\Users\liowk\Documents\mcp server"
    )
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            if tool_name == "get_weather":
                res = await session.call_tool("get_weather", {"city": tool_input})
                return f"Used tool (get_weather)\nCONTENT: {res.content[0].text}"
            elif tool_name == "search_news":
                args = tool_input.split(',',1)
                res = await session.call_tool("search_news", {"query": args[0], "country": args[1].strip()})
                if "No articles found for query=" in res.content[0].text:
                    return f"Used tool (search_news), no articles found\nCONTENT: {res.content[0].text}"
                return f"Used tool (search_news)\nCONTENT: {res.content[0].text}"
            elif tool_name == "analyze_sentiment":
                res = await session.call_tool("analyze_sentiment", {"text": tool_input})
                return f"Used tool (analyze_sentiment)\nCONTENT: {res.content[0].text}"
            elif tool_name == "search_documents":
                res = await session.call_tool("search_documents", {"query": tool_input})
                return f"Used tool (search_documents)\nCONTENT: {res.content[0].text}"

def calculator(expression: str):
    stack = []
    for char in expression.split(' '):
        try:
            stack.append(float(char))
        except ValueError:
            num2 = stack.pop()
            num1 = stack.pop()
            if char == '+':
                stack.append(num1 + num2)
            elif char == '-':
                stack.append(num1 - num2)
            elif char == '*':
                stack.append(num1 * num2)
            elif char == '/':
                stack.append(num1 / num2)
    return str(stack[0])

def read_file(path: str):
    try:
        with open(path,'r') as file:
            f = file.read()

        return f
    except FileNotFoundError:
        return f"Error: file path {path} not found"

def write_file(path: str, content: str):
    with open(path,'w') as file:
        file.write(content.replace("\\n","\n"))
    return f"Content successfully written to {path}"

def web_search(query: str):
    tavily_client = TavilyClient(os.getenv("TAVILY_API_KEY"))
    response = tavily_client.search(
        query = query,
        search_depth = "advanced",
        max_results = 1,
    )
    return f'Fetched {response["results"][0]["url"]}\nCONTENT: {response["results"][0]["content"]}'

def run_tools(tool_name: str, tool_input: str):
    if tool_name == "calculator":
        return calculator(tool_input)
    elif tool_name == "read_file":
        return read_file(tool_input)
    elif tool_name == "write_file":
        args = tool_input.split(',',1)
        return write_file(args[0], args[1].strip())
    elif tool_name == "web_search":
        return web_search(tool_input)
    elif tool_name in ["get_weather", "search_news", "analyze_sentiment", "search_documents"]:
        return asyncio.run(mcp_server(tool_name, tool_input))
    else:
        return f"Error: tool {tool_name} unavailable"

def main():
    prompt = input("User: ")
    messages = [{"role": "user", "content": prompt}]

    while len(messages) < 20:
        response = client.messages.create(
            model = "claude-haiku-4-5-20251001",
            max_tokens = 1024,
            system = """<instructions>You are a helpful assistant that always respond ONLT in the given format. DO NOT explain. You will be given a list of tools and it's required arguments.
            You MUST follow this rule absolutely: output EXACTLY ONE Thought. If tools required: ONE Action, and ONE Action Input per response. STOP immediately after Action Input. Do NOT output multiple actions. Do NOT output FINISH in the same response as an Action. Wait for the Observation before continuing.<instructions>
    <format>Thought: chain of thoughts when responding
    Action: name of tool you choose to use (respond this line if only tool is used)
    Action Input: tool argument (respond this line if only tool is used)
    FINISH: final response (DO NOT include this line if Action is used. Respond this line if you believe that the final response is complete)</format>
    <tools>Tool 1: calculator, Args: Postfix arithmetic operation with +, -, * and / only, with every number and operator seperated by a space.
    Tool 2: read_file, Args: File path to read for file content
    Tool 3: write_file, Args: File path to write file contents to and contents to write into the file. Both args seperated by a comma. Contents must be on a single line, use \n for newlines.
    Tool 4: web_search, Args: Query to search for in the web.
    Tool 5: get_weather, Args: Name of a city for it's respective weather data.
    Tool 6: search_news, Args: Query of news to search for and the respective country for the news. Both args seperated by a comma.
    Tool 7: analyze_sentiment, Args: Text to analyze sentiment of.
    Tool 8: search_documents, Args: Query related to BanG Dream to search from a database of BanG Dream data.</tools>""",
            messages = messages
        )
        result = next((b.text for b in response.content if b.type == 'text'),'')
        print('\n' + result)
        messages.append({"role": "assistant", "content": result})

        for line in result.split('\n'):
            if 'FINISH: ' in line:
                break
            elif 'Action Input: ' in line:
                args = line[14:]
                tool_result = run_tools(tool_name,args)
                res = f"\nObservation: {tool_result}"
                index = res.find("\nCONTENT: ")
                if index != -1:
                    print(res[:index])
                else:
                    print(res)
                messages.append({"role": "user", "content": res})
            elif 'Action: ' in line:
                tool_name = line[8:]
        if 'FINISH: ' in result:
            break
        
if __name__ == '__main__':
    main()

