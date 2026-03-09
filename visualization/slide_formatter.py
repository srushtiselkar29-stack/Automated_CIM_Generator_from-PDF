from typing import List, Dict
import re

from pptx import text


class SlideFormatter:
    """
    Formats LLM generated summaries into structured slide content
    """

    def format_slides(self, slides: List[Dict]) -> List[Dict]:

        formatted_slides = []

        for slide in slides:

            title = self._clean_title(slide.get("title", "Slide"))

            visual = slide.get("visual", "bullets")

            content = slide.get("content", "")

            if visual == "metrics":
                metrics = self._extract_metrics(content)

                formatted_slides.append({
                    "title": title,
                    "visual": "metrics",
                    "metrics": metrics
                })

            elif visual == "chart" or self._contains_numbers(content):

                categories, values = self._extract_chart_data(content)

                chart_type = self._decide_chart_type(content)

                formatted_slides.append({
                    "title": title,
                    "visual": "chart",
                    "chart_type": chart_type,
                    "categories": categories,
                    "values": values
                })

            elif visual == "image":

                bullets = self._format_bullets(content)

                formatted_slides.append({
                    "title": title,
                    "visual": "image",
                    "content": bullets
                })

            else:

                bullets = self._format_bullets(content)

                formatted_slides.append({
                    "title": title,
                    "visual": "bullets",
                    "content": bullets
                })

        return formatted_slides

    # -----------------------------------------------------

    def _contains_numbers(self, text: str) -> bool:

        numbers = re.findall(r"\d+", text)

        return len(numbers) >= 3
    
    def _clean_title(self, title: str) -> str:

        title = title.strip()
        title = title.replace("\n", " ")

        return title

    # -----------------------------------------------------

    def _format_bullets(self, text: str) -> str:

        lines = text.split("\n")

        bullets = []

        for line in lines:

            line = line.strip()

            if not line:
                continue

            if not line.startswith("•"):
                line = "• " + line

            bullets.append(line)

        return "\n".join(bullets)

    # -----------------------------------------------------

    def _extract_metrics(self, text: str) -> List[str]:

        """
        Extract numbers / financial metrics
        """

        lines = text.split("\n")

        metrics = []

        pattern = r"\$?\d+(\.\d+)?%?|\d+\s?(million|billion|M|B)"

        for line in lines:

            if re.search(pattern, line, re.IGNORECASE):

                clean = line.strip()

                metrics.append(clean)

        if not metrics:

            metrics = lines[:3]

        return metrics[:3]

    # -----------------------------------------------------

    def _extract_chart_data(self, text: str):

        """
        Extract simple chart data from text
        """

        numbers = re.findall(r"\d+", text)

        values = [int(n) for n in numbers[:4]]

        if not values:
            values = [100, 120, 150, 180]

        categories = [f"Item {i+1}" for i in range(len(values))]

        return categories[:len(values)], values
    
    def _decide_chart_type(self, text: str) -> str:

        text = text.lower()

        if "trend" in text or "growth" in text or "over time" in text:
            return "line"

        if "distribution" in text or "share" in text or "%" in text:
            return "pie"

        if "comparison" in text or "compare" in text:
            return "bar"

        return "bar"