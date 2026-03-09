from utils.pdf_reader import PDFReader
from utils.text_chunker import TextChunker

from models.embedding_model import EmbeddingModel
from models.llm_engine import LLMEngine

from storage.vector_store import VectorStore

from visualization.slide_formatter import SlideFormatter

from models.slide_schema import SlideContent 
import random


class ReportPipeline:
    """
    End-to-end report processing pipeline
    """

    def __init__(self, pdf_path: str):

        self.pdf_path = pdf_path

        self.pdf_reader = PDFReader(pdf_path)
        self.chunker = TextChunker()

        self.embedding_model = EmbeddingModel()
        self.llm = LLMEngine()

        self.vector_store = VectorStore()

        self.formatter = SlideFormatter()

    def rerank_chunks(self, goal, chunks):

        goal_words = set(goal.lower().split())

        scored_chunks = []

        for chunk in chunks:
            words = set(chunk.lower().split())
            score = len(goal_words.intersection(words))
            scored_chunks.append((score, chunk))

        scored_chunks.sort(reverse=True)

        return [c[1] for c in scored_chunks]
    
    def detect_sections(self, chunks):

        sections = {}

        current_section = "general"

        for chunk in chunks:

            if "market" in chunk.lower():
                current_section = "market"

            elif "financial" in chunk.lower():
                current_section = "financial"

            elif "risk" in chunk.lower():
                current_section = "risk"

            elif "product" in chunk.lower():
                current_section = "products"

            sections.setdefault(current_section, []).append(chunk)

        return sections

    def run(self):

        # -------------------------
        # 1. Extract PDF text
        # -------------------------

        text = self.pdf_reader.extract_text()

        print("\n========== PDF TEXT PREVIEW ==========\n")
        print(text[:1500])
        print("\n======================================\n")
        print("Total characters extracted:", len(text))

        # -------------------------
        # 2. Chunk document
        # -------------------------

        chunks = self.chunker.split_text(text)

        sections = self.detect_sections(chunks)

        # -------------------------
        # 3. Create embeddings
        # -------------------------

        embeddings = self.embedding_model.embed_documents(chunks)

        # -------------------------
        # 4. Store vectors
        # -------------------------

        self.vector_store.add_documents(chunks, embeddings)

        # -------------------------
        # 5. Document Intelligence
        # -------------------------

        sampled_chunks = random.sample(chunks, min(20, len(chunks)))
        context = "\n".join(sampled_chunks)

        insights = self.llm.analyze_document(context)

        # -------------------------
        # 6. Slide Planning
        # -------------------------

        slide_plan = self.llm.create_slide_plan(insights)

        # -------------------------
        # 7. Generate Slides
        # -------------------------

        slides = []

        for slide in slide_plan:

            goal = f"{slide['title']} - {slide['goal']}"

            query_vector = self.embedding_model.embed_text(goal)

            retrieved_chunks = self.vector_store.search(
                query_vector,
                top_k=20
            )

            # normalize search results
            retrieved_chunks = [
                c[0] if isinstance(c, tuple)
                else c["text"] if isinstance(c, dict)
                else c
                for c in retrieved_chunks
            ]

            relevant_chunks = self.rerank_chunks(goal, retrieved_chunks)[:10]

            # fallback if retrieval weak
            if not relevant_chunks:
                relevant_chunks = random.sample(chunks, min(6, len(chunks)))

            context = "\n\n".join(relevant_chunks)

            slide_content = self.llm.generate_slide(
                context=context,
                goal=goal
            )

            # Ensure slide_content is a Pydantic object
            if isinstance(slide_content, dict):
                slide_content = SlideContent(**slide_content)

            clean_bullets = [
                b for b in slide_content.bullets
                if not b.lower().startswith(("slide", "title"))
            ]

            metrics = slide_content.metrics or []

            metric_text = "\n".join([f"• {m}" for m in metrics[:2]])

            content = "\n".join(clean_bullets[:3])

            if metric_text:
                content = content + "\n\nKey Metrics:\n" + metric_text

            title = slide_content.headline.strip()
            if len(title) > 80:
                title = title[:80] + "..."

            slides.append({
                "title": slide_content.headline,
                "content": content,
                "visual": slide_content.visual,
                "metrics": metrics
            })

            

        # -------------------------
        # 8. Format slides
        # -------------------------

        slides = self.formatter.format_slides(slides)

        return slides