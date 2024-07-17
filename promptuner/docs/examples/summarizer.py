from promptuner import Prompt   
from promptuner.decorators import *

import json
 

if __name__ == "__main__":
    # Define the task
    TASK = "Create a summary of the given passage, focusing on the specified key points. The summary should be approximately the specified word count."

    # Initialize a new Prompt
    prompt = Prompt(TASK, variables=["PASSAGE", "KEY_POINTS", "WORD_COUNT"])
    
    prompt.apply_decorator([Thinking(repeat=2), ResultWrapper(repeat=2, tag="summary"), JsonResponse()])

    # Train the prompt
    prompt.train(answer_tag="summary")

    # Print the generated prompt template
    print("Generated Prompt Template:")
    print(prompt.prompt)

    # Load a sample passage
    SAMPLE_PASSAGE = """
In 1955, Rosa Parks, a prominent figure in the American civil rights movement, refused to give up her bus seat to a white passenger in Montgomery, Alabama. This act of defiance sparked the Montgomery Bus Boycott, a pivotal event in the struggle for racial equality. The boycott was organized by the Montgomery Improvement Association, led by a young pastor named Martin Luther King Jr.

King's leadership during the 381-day boycott catapulted him to national prominence. His advocacy for nonviolent resistance, inspired by Mahatma Gandhi's philosophy, became a cornerstone of the civil rights movement. The boycott eventually led to a United States Supreme Court decision that declared the Alabama bus segregation laws unconstitutional.

The success of the Montgomery Bus Boycott encouraged further civil rights activities, including the founding of the Southern Christian Leadership Conference (SCLC) in 1957. King served as the SCLC's first president, working alongside other activists like Ralph Abernathy and Bayard Rustin to coordinate nonviolent protests against racist policies across the American South.

These events set the stage for larger demonstrations, culminating in the 1963 March on Washington for Jobs and Freedom. At this historic gathering, King delivered his famous "I Have a Dream" speech at the Lincoln Memorial, solidifying his place as a central figure in American history and the global struggle for human rights.
"""

    # Define key points and word count
    KEY_POINTS = "main argument, supporting evidence, and conclusion"
    WORD_COUNT = "150"

    # Use the prompt to generate a summary
    response = prompt(
        variable_values={
            "PASSAGE": SAMPLE_PASSAGE,
            "KEY_POINTS": KEY_POINTS,
            "WORD_COUNT": WORD_COUNT
        },
        model_name="claude-3-5-sonnet-20240620"
    )

    print("\nGenerated Summary:")
    print(response['summary'])

    # Save the prompt
    prompt.save("data/saved_prompt.json")

    # Optionally, load the saved prompt
    # loaded_prompt = Prompt.load("data/saved_prompt.json")
    # print("\nLoaded Prompt Template:")
    # print(loaded_prompt.prompt)