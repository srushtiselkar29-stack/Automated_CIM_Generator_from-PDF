import json
import re


def extract_json(text):
    """
    Extract JSON object or list from LLM output safely
    """

    if not text:
        return None

    # remove markdown
    text = text.replace("```json", "").replace("```", "").strip()

    # try direct parse
    try:
        return json.loads(text)
    except Exception:
        pass

    # find first { and last }
    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1:
        candidate = text[start:end+1]

        try:
            return json.loads(candidate)
        except Exception:
            pass

    # find first [ and last ]
    start = text.find("[")
    end = text.rfind("]")

    if start != -1 and end != -1:
        candidate = text[start:end+1]

        try:
            return json.loads(candidate)
        except Exception:
            pass

    return None