from openai import OpenAI
import os

class agent: 
    def __init__(self):
        self.client = OpenAI(
        base_url="https://api.tokenfactory.nebius.com/v1/",
        api_key=os.environ.get("NEBIUS_API_KEY")
)
    
    def nebiusAgent(self,message):
        print("Please wait while your code gets processed by the Nvidia Agent")
        try:
            response = self.client.chat.completions.create(
                model="nvidia/nemotron-3-super-120b-a12b",
                messages=[
                    {
                        "role": "user",
                        "content": message
                    }
                ],
                max_tokens=50000
            )
        except Exception as E:
            return ("Error with agent. Please try again later")
        return response.choices[0].message.content
        


