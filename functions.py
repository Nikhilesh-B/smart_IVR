functions = [
                {
                    'name':'submit_ticket',
                    'description':"Given a conversation between an agent and a customer. Submit the relevant information about the customer's concern to the system",
                    "properties" :{
                        "type":"object",
                        "customer_name":{
                            "type":"string",
                            "description": "The first name and last name of the customer",
                        },
                        "agent_name":{
                            "type":"string",
                            "description": "The first name and last name of the agent helping the customer",
                        },
                        "summary":{
                            "type":"string",
                            "description": "A summary of the main topic of the converation",
                        },
                        "resolved":{
                            "type":"boolean",
                            "description": "Whether the agent was able to provide an end to end resolution of the customer's problem"
                        },
                        "required": ["customer_name", "agent_name", "summary","resolved"]
                        }
                }
            ]