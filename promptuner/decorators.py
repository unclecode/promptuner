DECORATOR_TEMPLATE = """\n\n# VERY IMPORTANT >> Consider the extra following points for the task:"""

RESULT_WRAPPER = """## Result XML Tag Wrapper: ALWAYSE wrap up the main requested answer in <result></result> XML tag, make sure to include it in the final answer. For example, if the task asks to review an article and then generate a summary, the final summary should be wrapped in <result> tags, while rest of the content, including thinking and analysis or other things should be outside of <result> tags. DO NOT USE any other XML tags for the final answer, only <result> tags."""
THINKING = """## Thinking Scratchpad: If the task is particularly complicated, you may wish to instruct the AI to think things out beforehand using <scratchpad>, <thinking> or <inner monologue> XML tags before it gives its final answer. Just for very simple tasks, doen'n''t need such self-reflection or thinking, omit this part."""
MUST_THINKING = """## Thinking Scratchpad: Instruct the AI to think things out beforehand using <scratchpad>, <thinking> or <inner monologue> XML tags before it gives its final answer. Remember don't use this for yourself, I am asking you to instruct the AI to use this in the final prompt to solve the task."""
JSON_RESPONSE = """## JSON Response: Make sure the final response within the specified XML tag is well JSON formatted, following the provides schema in the tesk definition. This should be a parsable and error-free JSON response wrapped in specified XML tag."""

from abc import ABC, abstractmethod
from typing import Any
import json
from .utils import extract_xml_data, split_and_parse_json_objects

class BaseDecorator(ABC):
    def __init__(self, repeat: int = 1):
        self.repeat = repeat
        pass
    
    @abstractmethod
    def call(self, prompt: str) -> str:
        pass
    
    def __call__(self, prompt: str) -> str:
        return prompt + self.repeat * self.call(prompt)

    def parse_response(self, response: Any) -> str:
        return response  # Default implementation is identity function

class ResultWrapper(BaseDecorator):
    def __init__(self, tag: str = "result", repeat: int = 1):
        super().__init__(repeat)
        self.tag = tag

    def call(self, prompt: str) -> str:
        content = RESULT_WRAPPER.replace("<result>", f"<{self.tag}>").replace("</result>", f"</{self.tag}>")
        return f"\n\n{content}"

    def parse_response(self, response: str) -> str:
        return extract_xml_data([self.tag], response)[self.tag]

class Thinking(BaseDecorator):
    def call(self, prompt: str) -> str:
        return "\n\n{}".format(THINKING)

class MustThinking(BaseDecorator):
    def call(self, prompt: str) -> str:
        return "\n\n{}".format(MUST_THINKING)

class JsonResponse(BaseDecorator):
    def call(self, prompt: str) -> str:
        return "\n\n{}".format(JSON_RESPONSE)

    def parse_response(self, response: str) -> str:
        try:
            content = json.loads(response)
        except json.JSONDecodeError:
            parsed, _ = split_and_parse_json_objects(response)
            content = parsed
        return json.dumps(content, indent=4)

SCRATCHPAD = """## SCRATCHPAD: The SCRATCHPAD technique encourages thorough thought processes before providing a final answer. It involves explicitly instructing the AI to use a designated space for preliminary thinking and analysis.

Modify the prompt to include the following instructions:

1. Before providing your final answer, use a <thinking></thinking> section as a scratchpad.
2. Within these tags, break down the task, consider different aspects, and explore your reasoning process.
3. Use this space to:
   - Analyze the given information
   - Consider multiple approaches or perspectives
   - Identify potential challenges or edge cases
   - Develop a structured approach to solving the task
4. After your thorough analysis in the <thinking> section, provide your final, refined answer wrapped in <result> tags.

Emphasize that the content within <thinking> tags should be a visible part of the response, allowing for transparency in the problem-solving process. The final, concise answer should then be presented within <result> tags.

Here's a general structure to suggest:

<thinking>
[Detailed analysis and thought process here]
</thinking>

<result>
[Final, refined answer based on the thinking process]
</result>

Encourage a balance between comprehensive thinking and concise final answers."""

class Scratchpad(BaseDecorator):
    def call(self, prompt: str) -> str:
        return f"\n\n{SCRATCHPAD}"


COT = """## Chain-of-Thought: Incorporate Chain-of-Thought reasoning into the prompt. This technique encourages the AI to break down complex problems into step-by-step reasoning processes. When generating the prompt, include instructions for the AI to:

1. Explicitly state its thought process.
2. Break down the problem into smaller, manageable steps.
3. Show its reasoning for each step.
4. Explain how each step leads to the next.
5. Summarize its conclusions based on this step-by-step analysis.

For example, instead of just asking for a final answer, the prompt should instruct the AI to think through the problem like this:

"Let's approach this step-by-step:
1. First, we need to understand...
2. Given this information, we can deduce...
3. The next logical step is to...
4. Considering all these factors, we can conclude..."

This approach helps in generating more accurate and transparent responses, especially for complex tasks. The final answer should still be wrapped in <result> tags, but the chain of thought leading to it should be visible."""

class ChainOfThought(BaseDecorator):
    def call(self, prompt: str) -> str:
        return f"\n\n{COT}"
    
FEW_SHOT = """## Few-Shot Learning: Few-Shot Learning is a technique where the AI is provided with a small number of examples to guide its understanding and response to a given task. This method helps the AI grasp the context and expected output format without extensive training.

Please add a section to the prompt that includes 2-3 diverse, synthetic examples relevant to the main task. These examples should:

1. Illustrate the type of input the AI might receive.
2. Demonstrate appropriate responses or solutions.
3. Cover different aspects or variations of the task, if applicable.

Generate these examples based on the main task description, ensuring they are clear and helpful in guiding the AI's understanding. The examples should be seamlessly integrated into the prompt, maintaining a natural flow with the rest of the content.

After providing the examples, instruct the AI to approach the main task in a similar manner to the given examples."""

class FewShotLearning(BaseDecorator):
    def call(self, prompt: str) -> str:
        return f"\n\n{FEW_SHOT}"
    
REACT = """## ReAct (Reasoning and Acting): ReAct is a problem-solving approach that combines reasoning and acting. It involves breaking down a task into a series of thought steps and actions, allowing for more structured and transparent problem-solving.

Incorporate the ReAct approach into the prompt by instructing to follow this pattern:

1. Thought: Analyze the current situation or problem.
2. Action: Decide on a specific action to take based on the analysis.
3. Observation: Describe the result or outcome of the action.
4. Repeat this cycle until the task is completed.

For complex tasks, generate a few example cycles of Thought-Action-Observation to demonstrate the process. Then, approach the main task using this ReAct method, clearly separating each step in the problem-solving process.

You may instruct the AI to ensure that the final conclusion or solution is still wrapped in <result> tags, while the reasoning process is visible outside of these tags."""

class ReAct(BaseDecorator):
    def call(self, prompt: str) -> str:
        return f"\n\n{REACT}"
    
OUTPUT_EXAMPLES = """# Output Examples

To improve the quality and relevance of the AI's responses, incorporate examples of the expected final output into the prompt. These examples should illustrate the desired format, style, and content of the response.

Add a section to the prompt that includes 2-3 diverse examples of high-quality outputs relevant to the main task. These examples should:

1. Demonstrate the expected structure and format of the output.
2. Showcase the appropriate level of detail and depth.
3. Illustrate any specific requirements or preferences for the output.
4. Cover different aspects or variations of the task, if applicable.

Generate these output examples based on the main task description. Ensure they are realistic, diverse, and aligned with the task's goals. Integrate the examples seamlessly into the prompt, clearly labeling them as example outputs.

After providing the examples, instruct to produce a response that follows a similar format and quality level as the given examples, while tailoring the content to the specific task at hand.

Remember to emphasize that while these are examples to guide the structure and quality, the actual response should be original and directly address the given task."""

class OutputExamples(BaseDecorator):
    def call(self, prompt: str) -> str:
        return f"\n\n{OUTPUT_EXAMPLES}"