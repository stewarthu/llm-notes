#!/usr/bin/env python
# coding: utf-8

# # How to call functions with chat models
# 
# This notebook covers how to use the Chat Completions API in combination with external functions to extend the capabilities of GPT models.
# 
# `functions` is an optional parameter in the Chat Completion API which can be used to provide function specifications. The purpose of this is to enable models to generate function arguments which adhere to the provided specifications. Note that the API will not actually execute any function calls. It is up to developers to execute function calls using model outputs.
# 
# If the `functions` parameter is provided then by default the model will decide when it is appropriate to use one of the functions. The API can be forced to use a specific function by setting the `function_call` parameter to `{"name": "<insert-function-name>"}`. The API can also be forced to not use any function by setting the `function_call` parameter to `"none"`. If a function is used, the output will contain `"finish_reason": "function_call"` in the response, as well as a `function_call` object that has the name of the function and the generated function arguments.
# 
# ### Overview
# 
# This notebook contains the following 2 sections:
# 
# - **How to generate function arguments:** Specify a set of functions and use the API to generate function arguments.
# - **How to call functions with model generated arguments:** Close the loop by actually executing functions with model generated arguments.

# ## How to generate function arguments

# In[ ]:


!pip install scipy
!pip install tenacity
!pip install tiktoken
!pip install termcolor 
!pip install openai
!pip install requests

# In[1]:


import json
import openai
import requests
from tenacity import retry, wait_random_exponential, stop_after_attempt
from termcolor import colored

GPT_MODEL = "gpt-3.5-turbo-0613"

# ### Utilities
# 
# First let's define a few utilities for making calls to the Chat Completions API and for maintaining and keeping track of the conversation state.

# In[2]:


@retry(wait=wait_random_exponential(min=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(messages, functions=None, function_call=None, model=GPT_MODEL):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + openai.api_key,
    }
    json_data = {"model": model, "messages": messages}
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


# In[3]:


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

# ### Basic concepts
# 
# Let's create some function specifications to interface with a hypothetical weather API. We'll pass these function specification to the Chat Completions API in order to generate function arguments that adhere to the specification.

# In[4]:


functions = [
    {
        "name": "get_current_weather",
        "description": "Get the current weather",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA",
                },
                "format": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "The temperature unit to use. Infer this from the users location.",
                },
            },
            "required": ["location", "format"],
        },
    },
    {
        "name": "get_n_day_weather_forecast",
        "description": "Get an N-day weather forecast",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA",
                },
                "format": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "The temperature unit to use. Infer this from the users location.",
                },
                "num_days": {
                    "type": "integer",
                    "description": "The number of days to forecast",
                }
            },
            "required": ["location", "format", "num_days"]
        },
    },
]

# If we prompt the model about the current weather, it will respond with some clarifying questions.

# In[5]:


messages = []
messages.append({"role": "system", "content": "Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous."})
messages.append({"role": "user", "content": "What's the weather like today"})
chat_response = chat_completion_request(
    messages, functions=functions
)
assistant_message = chat_response.json()["choices"][0]["message"]
messages.append(assistant_message)
assistant_message


# Once we provide the missing information, it will generate the appropriate function arguments for us.

# In[6]:


messages.append({"role": "user", "content": "I'm in Glasgow, Scotland."})
chat_response = chat_completion_request(
    messages, functions=functions
)
assistant_message = chat_response.json()["choices"][0]["message"]
messages.append(assistant_message)
assistant_message


# By prompting it differently, we can get it to target the other function we've told it about.

# In[7]:


messages = []
messages.append({"role": "system", "content": "Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous."})
messages.append({"role": "user", "content": "what is the weather going to be like in Glasgow, Scotland over the next x days"})
chat_response = chat_completion_request(
    messages, functions=functions
)
assistant_message = chat_response.json()["choices"][0]["message"]
messages.append(assistant_message)
assistant_message


# Once again, the model is asking us for clarification because it doesn't have enough information yet. In this case it already knows the location for the forecast, but it needs to know how many days are required in the forecast.

# In[8]:


messages.append({"role": "user", "content": "5 days"})
chat_response = chat_completion_request(
    messages, functions=functions
)
chat_response.json()["choices"][0]


# #### Forcing the use of specific functions or no function

# We can force the model to use a specific function, for example get_n_day_weather_forecast by using the function_call argument. By doing so, we force the model to make assumptions about how to use it.

# In[9]:


# in this cell we force the model to use get_n_day_weather_forecast
messages = []
messages.append({"role": "system", "content": "Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous."})
messages.append({"role": "user", "content": "Give me a weather report for Toronto, Canada."})
chat_response = chat_completion_request(
    messages, functions=functions, function_call={"name": "get_n_day_weather_forecast"}
)
chat_response.json()["choices"][0]["message"]


# In[10]:


# if we don't force the model to use get_n_day_weather_forecast it may not
messages = []
messages.append({"role": "system", "content": "Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous."})
messages.append({"role": "user", "content": "Give me a weather report for Toronto, Canada."})
chat_response = chat_completion_request(
    messages, functions=functions
)
chat_response.json()["choices"][0]["message"]


# We can also force the model to not use a function at all. By doing so we prevent it from producing a proper function call.

# In[11]:


messages = []
messages.append({"role": "system", "content": "Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous."})
messages.append({"role": "user", "content": "Give me the current weather (use Celcius) for Toronto, Canada."})
chat_response = chat_completion_request(
    messages, functions=functions, function_call="none"
)
chat_response.json()["choices"][0]["message"]


# ## How to call functions with model generated arguments
# 
# In our next example, we'll demonstrate how to execute functions whose inputs are model-generated, and use this to implement an agent that can answer questions for us about a database. For simplicity we'll use the [Chinook sample database](https://www.sqlitetutorial.net/sqlite-sample-database/).
# 
# *Note:* SQL generation can be high-risk in a production environment since models are not perfectly reliable at generating correct SQL.

# ### Specifying a function to execute SQL queries
# 
# First let's define some helpful utility functions to extract data from a SQLite database.

# In[12]:


import sqlite3

conn = sqlite3.connect("data/Chinook.db")
print("Opened database successfully")

# In[13]:


def get_table_names(conn):
    """Return a list of table names."""
    table_names = []
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
    for table in tables.fetchall():
        table_names.append(table[0])
    return table_names


def get_column_names(conn, table_name):
    """Return a list of column names."""
    column_names = []
    columns = conn.execute(f"PRAGMA table_info('{table_name}');").fetchall()
    for col in columns:
        column_names.append(col[1])
    return column_names


def get_database_info(conn):
    """Return a list of dicts containing the table name and columns for each table in the database."""
    table_dicts = []
    for table_name in get_table_names(conn):
        columns_names = get_column_names(conn, table_name)
        table_dicts.append({"table_name": table_name, "column_names": columns_names})
    return table_dicts


# Now can use these utility functions to extract a representation of the database schema.

# In[14]:


database_schema_dict = get_database_info(conn)
database_schema_string = "\n".join(
    [
        f"Table: {table['table_name']}\nColumns: {', '.join(table['column_names'])}"
        for table in database_schema_dict
    ]
)

# As before, we'll define a function specification for the function we'd like the API to generate arguments for. Notice that we are inserting the database schema into the function specification. This will be important for the model to know about.

# In[15]:


functions = [
    {
        "name": "ask_database",
        "description": "Use this function to answer user questions about music. Output should be a fully formed SQL query.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": f"""
                            SQL query extracting info to answer the user's question.
                            SQL should be written using this database schema:
                            {database_schema_string}
                            The query should be returned in plain text, not in JSON.
                            """,
                }
            },
            "required": ["query"],
        },
    }
]

# ### Executing SQL queries
# 
# Now let's implement the function that will actually excute queries against the database.

# In[16]:


def ask_database(conn, query):
    """Function to query SQLite database with a provided SQL query."""
    try:
        results = str(conn.execute(query).fetchall())
    except Exception as e:
        results = f"query failed with error: {e}"
    return results

def execute_function_call(message):
    if message["function_call"]["name"] == "ask_database":
        query = json.loads(message["function_call"]["arguments"])["query"]
        results = ask_database(conn, query)
    else:
        results = f"Error: function {message['function_call']['name']} does not exist"
    return results

# In[17]:


messages = []
messages.append({"role": "system", "content": "Answer user questions by generating SQL queries against the Chinook Music Database."})
messages.append({"role": "user", "content": "Hi, who are the top 5 artists by number of tracks?"})
chat_response = chat_completion_request(messages, functions)
assistant_message = chat_response.json()["choices"][0]["message"]
messages.append(assistant_message)
if assistant_message.get("function_call"):
    results = execute_function_call(assistant_message)
    messages.append({"role": "function", "name": assistant_message["function_call"]["name"], "content": results})
pretty_print_conversation(messages)

# In[18]:


messages.append({"role": "user", "content": "What is the name of the album with the most tracks?"})
chat_response = chat_completion_request(messages, functions)
assistant_message = chat_response.json()["choices"][0]["message"]
messages.append(assistant_message)
if assistant_message.get("function_call"):
    results = execute_function_call(assistant_message)
    messages.append({"role": "function", "content": results, "name": assistant_message["function_call"]["name"]})
pretty_print_conversation(messages)

# ## Next Steps
# 
# See our other [notebook](How_to_call_functions_for_knowledge_retrieval.ipynb) that demonstrates how to use the Chat Completions API and functions for knowledge retrieval to interact conversationally with a knowledge base.
