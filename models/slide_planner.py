class SlidePlanner:

    def __init__(self, llm):
        self.llm = llm

    def create_plan(self, insights):

        prompt = f"""
You are preparing a CIM presentation for high-value clients.

Design a 10-slide deck.

Return JSON:

[
  {{
    "title": "...",
    "goal": "...",
    "visual": "chart | diagram | bullets | metrics | image"
  }}
]

Insights:
{insights}
"""

        return self.llm._call_huggingface(prompt)