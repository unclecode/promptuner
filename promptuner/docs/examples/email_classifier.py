import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from promptuner import Prompt
from promptuner.decorators import *
import json
 
 
if __name__ == "__main__":
    # Define the task
    TASK = """Analyze the given email content and perform the following:
    1. Classify the email into one of the provided class labels.
    2. Score the email's importance on a scale of 1 to 10.
    3. Provide a one-sentence summary of the email.
    4. Extract the sender's email address.
    Return the results in a JSON format."""

    # Initialize a new Prompt
    prompt = Prompt(TASK, variables=["EMAIL_CONTENT", "CLASS_LABELS"])
    
    # Check if prompt exists locally
    is_local = False
    if os.path.exists("data/email_analysis_prompt.json"):
        is_local = True
        prompt = Prompt.load("data/email_analysis_prompt.json")
    
    prompt.apply_decorator([
        Scratchpad(repeat=1),
        OutputExamples(repeat=1),
        ResultWrapper(repeat=1, tag="analysis"),
        JsonResponse()
    ])

    # Train the prompt
    if not is_local:
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
        # model_name="claude-3-5-sonnet-20240620"
        # model_name="ollama/llama3"
        model_name="ollama/phi3:latest"
        # model_name="ollama/qwen2:0.5b"
        # model_name="ollama/qwen2:1.5b"
    )

    print("\nEmail Analysis Results:")
    print(response['answer'])
    
    print("\nTags:")
    for tag, content in response['tags'].items():
        if tag != "analysis":
            print(f"<{tag}>\n{content}\n</{tag}>")

    print("\nRaw Response:")
    print(response['raw'])
    # Save the prompt
    prompt.save("data/email_analysis_prompt.json")

    # Optionally, load the saved prompt
    # loaded_prompt = Prompt.load("data/email_analysis_prompt.json")
    # print("\nLoaded Prompt Template:")
    # print(loaded_prompt.prompt)