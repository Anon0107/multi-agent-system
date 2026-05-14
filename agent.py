import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

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
        file.write(content.strip())
    return f"Content successfully written to {path}"

def run_tools(tool_name: str, tool_input: str):
    if tool_name == "calculator":
        return calculator(tool_input)
    elif tool_name == "read_file":
        return read_file(tool_input)
    elif tool_name == "write_file":
        args = tool_input.split(',',1)
        return write_file(args[0], args[1])
    else:
        return f"Error: tool {tool_name} unavailable"

def main():
    prompt = input("User: ")
    messages = [{"role": "user", "content": prompt}]

    while len(messages) < 20:
        response = client.messages.create(
            model = "claude-haiku-4-5-20251001",
            max_tokens = 1024,
            system = """<instructions>You are a helpful assistant that always respond ONLT in the given format. DO NOT explain. You will be given a list of tools and it's required arguments. You can ONLY use one tool at a time.<instructions>
    <format>Thought: chain of thoughts when responding
    Action: name of tool you choose to use (respond this line if only tool is used)
    Action Input: tool argument (respond this line if only tool is used)
    FINISH: final response (respond this line if you believe that the final response is complete)</format>
    <tools>Tool 1: calculator, Args: A string representing a postfix arithmetic operation with +, -, * and / only with every number and operator seperated by a space
    Tool 2: read_file, Args: A string representing a file path to read for file content
    Tool 3: write_file, Args: A string representing a file path to write file contents to and contents to write into the file. Both args seperated by a comma</tools>""",
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
                obs = f"\nObservation: {tool_result}"
                print(obs)
                messages.append({"role": "user", "content": obs})
            elif 'Action: ' in line:
                tool_name = line[8:]
        if 'FINISH: ' in result:
            break
        
if __name__ == '__main__':
    main()

