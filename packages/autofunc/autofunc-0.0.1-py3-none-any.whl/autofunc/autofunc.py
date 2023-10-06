import json
import openai
from pydantic import BaseModel

class AutoFunc():
    def __init__(self, system_instruction: str,
                 response_model: BaseModel = None,
                 model: str = "gpt-4-0613",
                 temperature: int = 0
                ):
        self.system_instruction = system_instruction
        self.model = model
        self.temperature = temperature
        self.response_model = response_model
        self.schema = response_model.model_json_schema() if response_model else {
            'properties': {'response_str': {'title': 'Response', 'type': 'string'}},
            'required': ['response_str'],
            'title': 'StrResponse',
            'type': 'object'
        }

    def __call__(self, input):
        response = openai.ChatCompletion.create(
            model=self.model,
            temperature=self.temperature,
            messages=[
               {"role": "system", "content": self.system_instruction},
               {"role": "user", "content": input}
            ],
            functions=[
                {
                  "name": "fn",
                  "description": "GPT function",
                  "parameters": self.schema
                }
            ],
            function_call={"name": "fn"}
        )
        response_args = json.loads(response.choices[0]["message"]["function_call"]["arguments"])
        return response_args if self.response_model else response_args['response_str']
