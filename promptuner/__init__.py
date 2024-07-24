# from .builder import *
import os, sys
import json
from typing import List, Dict, Union
import anthropic
import re
import litellm
from dotenv import load_dotenv
from .utils import *
from .config import *
from .decorators import *
load_dotenv()

class Prompt:
    def __init__(self, task: str, variables: List[str] = None, metaprompt: str = "default", model_name: str = None, api_key: str = None, **kwargs):
        self.task = task
        self.variables = variables or []
        self.decorators = []
        self.content = None
        self.token_count = None
        self.model_name = model_name or MODEL_NAME
        self.answer_tag = kwargs.get("answer_tag", "result")
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        
        if not self.api_key:
            raise ValueError("No API key provided. Make sure to set the ANTHROPIC_API_KEY environment variable or provide it as an argument.")
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
        
        # Load metaprompt
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        # Load metaprompt
        package_dir = os.path.dirname(os.path.abspath(__file__))
        metaprompts_dir = os.path.join(package_dir, "metaprompts")
        metaprompt_file = os.path.join(metaprompts_dir, f"{metaprompt}.md")
        try:
            with open(metaprompt_file, "r") as file:
                self.metaprompt = file.read()
        except FileNotFoundError:
            raise ValueError(f"Metaprompt file '{metaprompt}.md' not found")

    
    def apply_decorator(self, decorators: List[BaseDecorator]):
        self.decorators.extend(decorators)
            
    # Create funciton to remove specific decorators
    def remove_decorator(self, decorators: List[BaseDecorator]):
        for decorator in decorators:
            self.decorators.remove(decorator)
            
    def render(self):
        text = self.metaprompt + DECORATOR_TEMPLATE
        for decorator in self.decorators:
            text = decorator(text)
            
        return text
    
    def train(self,  **kwargs):
        variable_string = "\n".join("{" + variable.upper() + "}" for variable in self.variables)

        self.metaprompt = self.render()
        
        prompt = self.metaprompt.replace("{{TASK}}", self.task)
        assistant_partial = "<Inputs>"
        if variable_string:
            assistant_partial += variable_string + "\n</Inputs><Instructions Structure>"

        response = self.client.messages.create(
                model=self.model_name,
                max_tokens=4096,
                messages=[
                    {"role": "user", "content": prompt},
                    {"role": "assistant", "content": assistant_partial},
                ],
                temperature=0,
            )
        
        metaprompt_response = response.content[0].text
        output_tokens = response.usage.output_tokens
        self.token_count = output_tokens
        
        remove_empty_tags = lambda x: re.sub(r"<(\w+)></\1>$", "", x)
        
        between_tags = extract_between_tags("Instructions", metaprompt_response)[0]
        self.content = remove_empty_tags(between_tags).strip()
        
        pattern = r"{(.*)}"
        self.variables = list(set(re.findall(pattern, self.content)))

    def run(self, variable_values: Dict[str, str], model_name: str = None, api_key: str = None, **kwargs) -> Union[str, Dict]:
        return self(variable_values, model_name, api_key, **kwargs)
    
    def __call__(self, variable_values: Dict[str, str], model_name: str = None, api_key: str = None, **kwargs) -> Union[str, Dict]:
        if not self.content:
            raise ValueError("Prompt hasn't been trained yet. Call the train() method first.")
        
        prompt = self.replace_variables(variable_values)
        messages = [
            {"role": "user", "content": prompt},
        ]
        response = litellm.completion(
            model=model_name or self.model_name,
            messages=messages,
            api_key=api_key or self.api_key,
            num_retries=2,
            **kwargs
        )
        content = response.choices[0].message.content
        
        tags = extract_xml_tags(content)
        tags_contnet = extract_xml_data(tags, content)
        
        # Apply response parsing from decorators
        for decorator in self.decorators:
            content = decorator.parse_response(content)
        
        return {"answer": content, "tags": tags_contnet, "raw": response.choices[0].message.content}

    def replace_variables(self, variable_values: Dict[str, str]) -> str:
        prompt_with_variables = self.content
        for variable, value in variable_values.items():
            if variable not in self.variables:
                continue
            prompt_with_variables = prompt_with_variables.replace("{" + variable + "}", value)
        return prompt_with_variables

    def save(self, path: str):
        with open(path, "w") as file:
            json.dump({"task": self.task, "prompt": self.content, "variables": self.variables}, file)

    @staticmethod
    def load(path: str) -> "Prompt":
        with open(path, "r") as file:
            data = json.load(file)
            prompt = Prompt(data["task"])
            prompt.content = data["prompt"]
            prompt.variables = data["variables"]
            return prompt
        

