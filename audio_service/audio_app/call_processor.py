from django.db import models
import openai, requests
from tenacity import retry, wait_random_exponential, stop_after_attempt
import audio_app.mysecrets as secrets



openai.api_key = secrets.gpt_api_key
GPT_MODEL = "gpt-3.5-turbo-0613"

class Call_Processor():
    def __init__(self):
        self.functions =[
                {
                    'name':'submit_ticket',
                    'description':"Given a conversation between an agent and a customer. Submit the relevant information about the customer's concern to the system",
                    "parameters":{
                        "type": "object",
                        "properties" :{
                            "firstName":{
                                "type":"string",
                                "description": "The first name of the customer",
                            },
                            "lastName":{
                                "type":"string",
                                "description": "The last name of the customer",
                            },
                            "description":{
                                "type":"string",
                                "description": "A summary of the main topic of the converation",
                            },
                            "resolved":{
                                "type":"boolean",
                                "description": "Whether the agent was able to provide an end to end resolution of the customer's problem"
                            },
                            },
                    "required": ["customer_name", "agent_name", "summary","resolved"]
                        }
                }
            ]

    @retry(wait=wait_random_exponential(min=1, max=40), stop=stop_after_attempt(3))
    def chat_completion_request(self, messages, functions=None, function_call=None, model=GPT_MODEL):
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

