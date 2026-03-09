from typing import List
from huggingface_hub import InferenceClient
import json

from config import settings
from models.slide_schema import SlideContent
from utils.json_parser import extract_json


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
                    "content": "You are a financial analyst creating PowerPoint slides. You must output valid JSON only."
                },
                {"role": "user", "content": prompt}
            ],
            max_tokens=400,
            temperature=0.2
        )

        return response.choices[0].message.content

    # -----------------------------------------------------

    def generate_slide(self, context: str, goal: str):

        prompt = f"""
You are generating PowerPoint slide content.

Use the context below to create ONE slide.

Context:
{context}

Goal:
{goal}

Return VALID JSON ONLY.

Format:

{{
"headline": "Short slide title",
"bullets": [
"bullet point 1",
"bullet point 2",
"bullet point 3"
],
"visual": "bar_chart | line_chart | pie_chart | area_chart | metrics | bullets",
"metrics": ["number or statistic"]
}}

Rules:
- Output JSON only
- No markdown
- No explanations
"""

        response = self._call_huggingface(prompt)

        print("\n========== LLM RESPONSE ==========\n")
        print(response)
        print("\n=================================\n")

        data = extract_json(response)
        if not data:
            # try cleaning model tokens
            cleaned = response.replace("<|system|>", "").replace("<|assistant|>", "").replace("<|user|>", "")
            data = extract_json(cleaned)

        # If list returned, take first object
        if isinstance(data, list) and len(data) > 0:
            data = data[0]

        # Fallback if parsing fails
        if not isinstance(data, dict):
            print("⚠️ Failed to parse LLM response")

            data = {
                "headline": goal,
                "bullets": ["Content extracted from document"],
                "visual": "bullets",
                "metrics": []
            }

        # Normalize metrics
        metrics = []
        for m in data.get("metrics", []):
            if isinstance(m, dict):
                number = m.get("number", "")
                if m.get("percentage"):
                    number = f"{number}%"
                metrics.append(str(number))
            else:
                metrics.append(str(m))

        data["metrics"] = metrics

        return SlideContent(**data)

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

        response = self._call_huggingface(prompt)

        plan = extract_json(response)

        if isinstance(plan, list):
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