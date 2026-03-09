import json
from models.slide_schema import SlideContent

class SlideGenerator:

    def __init__(self, llm):
        self.llm = llm

        
    def generate_slide(self, context: str, goal: str) -> SlideContent:

        prompt = f"""
            Create structured slide content for an investor presentation.

            Goal of slide:
            {goal}

            Return JSON with fields:
            headline
            bullets (3-4)
            visual (bullets | metrics | chart | image)
            metrics (optional)

            Report Content:
            {context}
            """

        response = self._call_huggingface(prompt)

        try:
            data = json.loads(response)

            # Always convert to Pydantic object
            return SlideContent(**data)

        except Exception:

            bullets = response.split("\n")

            return SlideContent(
                headline="Key Insights",
                bullets=[b.strip() for b in bullets if b.strip()][:4],
                visual="bullets",
                metrics=None
            )