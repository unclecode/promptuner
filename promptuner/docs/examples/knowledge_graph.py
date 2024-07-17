import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from promptuner import Prompt   
from promptuner.decorators import *
import json

if __name__ == "__main__":
    # Define the task
    TASK = """Generate a knowledge graph from the given passage. Identify key entities and their relationships. 
The output should be a JSON object with the two keys, one is 'entities' and the other is 'relationships'. Each entiry should have a 'name' and 'type' and each relationship should have 'source', 'target' and 'type'. Ensure that all entities mentioned in relationships are also listed in the entities array."""

    # Initialize a new Prompt
    prompt = Prompt(TASK, variables=["PASSAGE"])
    
    # Check if prompt exists locally
    is_local = False
    if os.path.exists("data/knowledge_graph_prompt.json"):
        is_local = True
        prompt = Prompt.load("data/knowledge_graph_prompt.json")
    
    prompt.apply_decorator([ 
        Scratchpad(),
        OutputExamples(),
        ResultWrapper(tag="graph"),
        JsonResponse()
    ])

    # Train the prompt
    if not is_local:
        prompt.train()

    # Print the generated prompt template
    print("Generated Prompt Template:")
    print(prompt.prompt)
    prompt.save("data/knowledge_graph_prompt.json")
    
    # Sample passage
    PASSAGE = """
    The Industrial Revolution, which began in Britain in the late 18th century, was a period of great technological and social change. 
    It marked a major turning point in history; almost every aspect of daily life was influenced in some way. 
    In particular, average income and population began to exhibit unprecedented sustained growth. 
    The factory system, fueled by technological innovations like the steam engine developed by James Watt, led to increased productivity and urbanization. 
    This shift had profound effects on social structures, as rural populations migrated to cities in search of factory work. 
    However, the rapid industrialization also led to difficult working and living conditions for many workers, which eventually sparked labor movements and calls for reforms.
    """

    # Use the prompt to generate the knowledge graph
    response = prompt(
        variable_values={
            "PASSAGE": PASSAGE
        },
        model_name="claude-3-5-sonnet-20240620"
    )

    print("\nKnowledge Graph:")
    print(json.dumps(json.loads(response['answer']), indent=2))
    
    print("\nTags:")
    for tag, content in response['tags'].items():
        if tag != "graph":
            print(f"<{tag}>\n{content}\n</{tag}>")

    # Save the prompt
    prompt.save("data/knowledge_graph_prompt.json")