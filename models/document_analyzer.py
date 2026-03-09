class DocumentAnalyzer:

    def __init__(self, llm):
        self.llm = llm

    def analyze(self, chunks):

        context = "\n".join(chunks[:20])

        prompt = f"""
You are an investment banking analyst.

Analyze the report and extract structured insights.

Return:
- company overview
- products/services
- market opportunity
- financial highlights
- competitive advantage
- risks
- growth strategy

Report:
{context}
"""

        return self.llm._call_huggingface(prompt)