from typing import List
from huggingface_hub import InferenceClient
from config import settings
import json
from models.slide_schema import SlideContent


class LLMEngine:

    def __init__(self):

        self.provider = settings.LLM_PROVIDER
        self.model_name = settings.LLM_MODEL

        if self.provider == "huggingface":
            self.client = InferenceClient(
                model=self.model_name,
                token=settings.HF_TOKEN
            )

    # -----------------------------------------------------

    def _call_huggingface(self, prompt: str) -> str:

        response = self.client.chat_completion(
            messages=[
                {
                    "role": "system",
                    "content": "You are an investment banking analyst creating CIM presentation slides."
                },
                {"role": "user", "content": prompt}
            ],
            max_tokens=400
        )

        return response.choices[0].message.content

    # -----------------------------------------------------

    def generate_slide(self, context: str, goal: str):

        prompt = f"""
        You are creating slides for a professional investment presentation.
        
        Return ONLY valid JSON.
        
        Format:
        
        {{
         "headline": "short headline",
         "bullets": ["bullet1","bullet2","bullet3"],
         "visual": "bullets | chart | metrics | image",
         "metrics": ["optional metric"]
        }}
        
        Goal:
        {goal}
        
        Report:
        {context}
        """

        response = self._call_huggingface(prompt)

        try:
            return json.loads(response)
        except:
            return {
                "headline": "Key Insights",
                "bullets": response.split("\n")[:4],
                "visual": "bullets"
            }

    # -----------------------------------------------------

    def analyze_document(self, context: str):

        prompt = f"""
You are an investment banking analyst.

Analyze the following report and extract:

Company Overview
Products / Services
Market Opportunity
Financial Highlights
Competitive Advantage
Growth Strategy
Risks

Return structured text.

Report:
{context}
"""

        return self._call_huggingface(prompt)

    # -----------------------------------------------------

    def create_slide_plan(self, insights: str):

        prompt = f"""
Create a 10-slide CIM presentation structure.

Return JSON list.

Each slide must contain:
title
goal
visual type (bullets, chart, metrics, image)

Example:

[
 {{
  "title": "Executive Summary",
  "goal": "Summarize the investment opportunity",
  "visual": "bullets"
 }}
]

Insights:
{insights}
"""

        from utils.json_parser import extract_json

        response = self._call_huggingface(prompt)

        plan = extract_json(response)

        if plan:
            return plan

        # fallback
        return [
            {"title": "Executive Summary", "goal": "Overview", "visual": "bullets"},
            {"title": "Company Overview", "goal": "Describe company", "visual": "bullets"},
            {"title": "Market Opportunity", "goal": "Explain market", "visual": "chart"},
            {"title": "Products", "goal": "Explain products", "visual": "image"},
            {"title": "Business Model", "goal": "Revenue model", "visual": "bullets"},
            {"title": "Financial Highlights", "goal": "Show financials", "visual": "metrics"},
            {"title": "Competitive Advantage", "goal": "Explain moat", "visual": "bullets"},
            {"title": "Growth Strategy", "goal": "Future growth", "visual": "chart"},
            {"title": "Risks", "goal": "Explain risks", "visual": "bullets"},
            {"title": "Investment Opportunity", "goal": "Pitch investment", "visual": "bullets"}
        ]