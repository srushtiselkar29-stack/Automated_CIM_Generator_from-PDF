import json
import re


def extract_json(text):
    """
    Extract first valid JSON object or list from LLM output
    """

    # remove markdown code blocks
    text = text.replace("```json", "").replace("```", "")

    # try direct parse
    try:
        return json.loads(text)
    except:
        pass

    # find JSON array
    array_match = re.search(r"\[.*?\]", text, re.DOTALL)

    if array_match:
        try:
            return json.loads(array_match.group())
        except:
            pass

    # find JSON object
    object_match = re.search(r"\{.*?\}", text, re.DOTALL)

    if object_match:
        try:
            return json.loads(object_match.group())
        except:
            pass

    return None