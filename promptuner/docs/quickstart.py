from promptuner import promptuner, Prompt
import os, json
from pathlib import Path

__current__ = Path(os.path.dirname(__file__))

# Load example data
TASK = ""
with open(__current__ / "sample_task.md", "r") as file:
    TASK = file.read()

SAMPLE_PASSAGE = ""
with open(__current__ / "sample_passage.md", "r") as file:
    SAMPLE_PASSAGE = file.read()

variables = ["PASSAGE"]

# Create prompt
promptuner = promptuner()
prompt = promptuner(TASK, variables)
print(prompt.prompt)    

# Execute prompt    
print(prompt.replace_variables({"PASSAGE": SAMPLE_PASSAGE}))
result = prompt(
    model_name = "anthropic/claude-3-5-sonnet-20240620", 
    variable_values = {"PASSAGE": SAMPLE_PASSAGE}, 
    answer_tag = "result", json_response = True
)
print(json.dumps(result, indent=4))

# Test saving and loading prompt
prompt.save(__current__ / "prompt.json")
prompt = Prompt.load(__current__ / "prompt.json")
print(prompt.prompt)
