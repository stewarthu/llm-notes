import json
import openai
import requests
from tenacity import retry, wait_random_exponential, stop_after_attempt
from termcolor import colored

@retry(wait=wait_random_exponential(min=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(messages, functions=None, function_call=None, model = 'gpt-4-0613', temperature = 0):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + openai.api_key,
    }
    json_data = {"model": model, "messages": messages, "temperature": temperature}
    if functions is not None:
        json_data.update({"functions": functions})
    if function_call is not None:
        json_data.update({"function_call": function_call})
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=json_data,
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e

def pretty_print_conversation(messages):
    role_to_color = {
        "system": "red",
        "user": "green",
        "assistant": "blue",
        "function": "magenta",
    }
    formatted_messages = []
    for message in messages:
        if message["role"] == "system":
            formatted_messages.append(f"system: {message['content']}\n")
        elif message["role"] == "user":
            formatted_messages.append(f"user: {message['content']}\n")
        elif message["role"] == "assistant" and message.get("function_call"):
            formatted_messages.append(f"assistant: {message['function_call']}\n")
        elif message["role"] == "assistant" and not message.get("function_call"):
            formatted_messages.append(f"assistant: {message['content']}\n")
        elif message["role"] == "function":
            formatted_messages.append(f"function ({message['name']}): {message['content']}\n")
    for formatted_message in formatted_messages:
        print(
            colored(
                formatted_message,
                role_to_color[messages[formatted_messages.index(formatted_message)]["role"]],
            )
        )

def call_function(tools, function_call, verbose = True):
    """Call a function and return the output as a string."""
    name = function_call["name"]
    arguments_str = function_call["arguments"]
    if verbose:
        print("=== Calling Function ===")
        print(f"Calling function: {name} with args: {arguments_str}")
    tool = tools[name]
    argument_dict = json.loads(arguments_str)
    output = tool(**argument_dict)
    if verbose:
        print(f"Got output: {output}")
        print("========================")
    return output

def chat(model, tools, functions, message, prompt, temperature):
    messages = []
    messages.append({"role": "system", "content": prompt})
    messages.append({"role": "user", "content": message}) 
    chat_response = chat_completion_request(messages, functions=functions, model = model, temperature = temperature)
    print(chat_response.json())
    assistant_message = chat_response.json()["choices"][0]["message"]
    #print(assistant_message)
    messages.append(assistant_message)
    function_call = assistant_message['function_call']

    n_function_calls = 0
    while function_call is not None:

        if n_function_calls >= 10:
            print(f"Exceeded max function calls.")
            break

        function_message = call_function(tools, function_call, True)
        print(function_message)
        n_function_calls += 1
        messages.append({"role": "user", "content": function_message})

        if not isinstance(function_message, str):
            return messages

        chat_response = chat_completion_request(messages, functions=functions, model = model)
        print(chat_response.json())
        assistant_message = chat_response.json()["choices"][0]["message"]
        finish_reason = chat_response.json()["choices"][0]["finish_reason"]
        messages.append(assistant_message)

        #print(assistant_message)
        if finish_reason == 'stop':
            return messages
        elif finish_reason == 'function_call':
            function_call = assistant_message['function_call']
        else:
            return("Something is wrong....Please retry.")
    return messages
