import os
from openai import OpenAI

class Agent: 
    def __init__(self):
        self.client = OpenAI(
        base_url="https://api.tokenfactory.nebius.com/v1/",
        api_key=os.environ.get("NEBIUS_API_KEY")
)
    
    def nebiusAgent(self,message):
        response = self.client.chat.completions.create(
            model="nvidia/nemotron-3-super-120b-a12b",
            messages=[
                {
                    "role": "user",
                    "content": message
                }
            ]
        )
        print(response.choices[0].message.content)
        


