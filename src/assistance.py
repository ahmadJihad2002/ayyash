from openai import OpenAI
import os

# Get the API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")

class Assistance:
    def __init__(self,api_token) -> str:

        self.client = OpenAI(api_key=api_token)
                            

        self.assistant = self.client.beta.assistants.create(
            name="ayyash",
            instructions="You are a personal assistance developed by palestinian developers.",
            tools=[{"type": "code_interpreter"}],
            model="gpt-3.5-turbo-0125",
        )

    def send_msg(self,msg):
        completion = self.client.chat.completions.create(
        temperature=0.3 , # Medium temperature for balanced response
        model="gpt-3.5-turbo",
        max_tokens=30,
        messages=[
          {"role": "system", "content": "ure name is ayyash, funnay, can make stunning, nice conversation, responds with short answers"},
          {"role": "user", "content": msg}
        ]
        )
        return completion.choices[0].message.content 
 
                    
Assistance = Assistance(api_token=api_key)

