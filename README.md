# Promptuner
## Turning small task descriptions into mega prompts automatically 🪄✨

🚀 **promptuner** is an open-source library that converts simple task descriptions into detailed, high-quality prompts for any large language model. With promptuner, even small models can achieve remarkable results by extracting perfect JSON, making function calls, creating structured outputs, and performing complex reasoning and analytical tasks.

## Features

- **Automagically Convert Task Descriptions**: Turn small task descriptions into professional, detailed prompts effortlessly.
- **Enhanced Performance**: Get the most out of your models, even small ones, with fine-tuned prompts.
- **Supports Complex Tasks**: Generate prompts for tasks requiring reasoning, chain of thoughts, and other analytical methods.
- **Execute Prompts**: Ability to execute the generated prompts for you.

## Getting Started

### Installation

To install promptuner, use pip:

```bash
pip install git+https://github.com/unclecode/promptuner.git
```

### Usage

Here's a basic example of how to use promptuner:

```python
from promptuner import Prompt
from promptuner.decorators import *
 
# Define the task
TASK = """Analyze the given email content and perform the following:
1. Classify the email into one of the provided class labels.
2. Score the email's importance on a scale of 1 to 10.
3. Provide a one-sentence summary of the email.
4. Extract the sender's email address.
Return the results in a JSON format."""

# Initialize a new Prompt
prompt = Prompt(TASK, variables=["EMAIL_CONTENT", "CLASS_LABELS"])
prompt.apply_decorator([
    Scratchpad(repeat=1),
    OutputExamples(repeat=1),
    ResultWrapper(repeat=1, tag="analysis"),
    JsonResponse()
])

# Train the prompt
prompt.train()

# Print the generated prompt template
print("Generated Prompt Template:")
print(prompt.prompt)
prompt.save("data/email_analysis_prompt.json")

# Sample email content
EMAIL_CONTENT = """
From: john.doe@example.com
Subject: Urgent: Project Deadline Extension Request

Dear Team,

I hope this email finds you well. I'm writing to request an extension for the upcoming project deadline. Due to unforeseen circumstances, including a critical team member's illness and some technical challenges we've encountered, we're slightly behind schedule.

We've made significant progress, but we need an additional week to ensure we deliver a high-quality product. I believe this extension will allow us to address all remaining issues and exceed your expectations.

Please let me know if you need any further information or if you'd like to discuss this matter in more detail. I appreciate your understanding and look forward to your response.

Best regards,
John Doe
Project Manager
"""

# Define class labels
CLASS_LABELS = "Work-related, Personal, Spam, Urgent, Newsletter, Other"

# Use the prompt to analyze the email
response = prompt(
    variable_values={
        "EMAIL_CONTENT": EMAIL_CONTENT,
        "CLASS_LABELS": CLASS_LABELS
    },
    model_name="ollama/phi3:latest"
    # model_name="claude-3-5-sonnet-20240620"
    # model_name="ollama/llama3"
    # model_name="ollama/qwen2:0.5b"
    # model_name="ollama/qwen2:1.5b"
)

print("\nEmail Analysis Results:")
print(response['answer'])

print("\nTags:")
for tag, content in response['tags'].items():
    if tag != "analysis":
        print(f"<{tag}>\n{content}\n</{tag}>")
```
For more examples check the `docs/examples` folder.

## Stay Tuned

We're currently working on detailed documentation and additional features. Please stay tuned as we finalize these resources over the next few days.

## Contributing

We welcome contributions from the community. If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request.

## License

promptuner is licensed under the Apache 2.0 License.

