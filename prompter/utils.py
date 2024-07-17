import re
from typing import List

def pretty_print(message):
    print(
        "\n\n".join(
            "\n".join(
                line.strip()
                for line in re.findall(r".{1,100}(?:\s+|$)", paragraph.strip("\n"))
            )
            for paragraph in re.split(r"\n\n+", message)
        )
    )

def split_and_parse_json_objects(json_string):
    """
    Splits a JSON string which is a list of objects and tries to parse each object.
    
    Parameters:
    json_string (str): A string representation of a list of JSON objects, e.g., '[{...}, {...}, ...]'.
    
    Returns:
    tuple: A tuple containing two lists:
        - First list contains all successfully parsed JSON objects.
        - Second list contains the string representations of all segments that couldn't be parsed.
    """
    # Trim the leading '[' and trailing ']'
    if json_string.startswith('[') and json_string.endswith(']'):
        json_string = json_string[1:-1].strip()
    
    # Split the string into segments that look like individual JSON objects
    segments = []
    depth = 0
    start_index = 0
    
    for i, char in enumerate(json_string):
        if char == '{':
            if depth == 0:
                start_index = i
            depth += 1
        elif char == '}':
            depth -= 1
            if depth == 0:
                segments.append(json_string[start_index:i+1])
    
    # Try parsing each segment
    parsed_objects = []
    unparsed_segments = []
    
    for segment in segments:
        try:
            obj = json.loads(segment)
            parsed_objects.append(obj)
        except json.JSONDecodeError:
            unparsed_segments.append(segment)
    
    return parsed_objects, unparsed_segments


def extract_between_tags(tag: str, string: str, strip: bool = False) -> list[str]:
    ext_list = re.findall(f"<{tag}>(.+?)</{tag}>", string, re.DOTALL)
    if strip:
        ext_list = [e.strip() for e in ext_list]
    return ext_list


def remove_empty_tags(text):
    return re.sub(r"<(\w+)></\1>$", "", text)


def extract_prompt(metaprompt_response):
    between_tags = extract_between_tags("Instructions", metaprompt_response)[0]
    return remove_empty_tags(remove_empty_tags(between_tags).strip()).strip()


def extract_variables(prompt):
    pattern = r"{([^}]+)}"
    variables = re.findall(pattern, prompt)
    return set(variables)


def extract_xml_tags(string):
    tags = re.findall(r'<(\w+)>', string)
    return list(set(tags))

def extract_xml_data(tags, string):
    data = {}

    for tag in tags:
        pattern = f"<{tag}>(.*?)</{tag}>"
        match = re.search(pattern, string, re.DOTALL)
        if match:
            data[tag] = match.group(1).strip()
        else:
            data[tag] = ""

    return data

