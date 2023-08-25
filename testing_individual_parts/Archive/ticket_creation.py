import openai, requests
from tenacity import retry, wait_random_exponential, stop_after_attempt
from termcolor import colored
from functions import functions
from conversation import CONVERSATION 
import json

openai.api_key = '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'
GPT_MODEL = "gpt-3.5-turbo-0613"

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
from pprint import pprint

if __name__ == "__main__":
    messages = []
    messages.append({"role":"system",
                     "content":"Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous."})
    messages.append({"role":"user", "content":CONVERSATION})
    response = chat_completion_request(messages, functions=functions)
    print(response.json())
    assistant_message = response.json()["choices"][0]["message"]
    pprint(assistant_message)