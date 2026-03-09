from utils.pdf_reader import PDFReader
from utils.text_chunker import TextChunker

from models.embedding_model import EmbeddingModel
from models.llm_engine import LLMEngine

from storage.vector_store import VectorStore

from visualization.slide_formatter import SlideFormatter

from models.slide_schema import SlideContent 


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

    def run(self):

        # -------------------------
        # 1. Extract PDF text
        # -------------------------

        text = self.pdf_reader.extract_text()

        # -------------------------
        # 2. Chunk document
        # -------------------------

        chunks = self.chunker.split_text(text)

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

        context = "\n".join(chunks[:20])

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

            goal = slide["goal"]

            query_vector = self.embedding_model.embed_text(goal)

            relevant_chunks = self.vector_store.search(
                query_vector,
                top_k=5
            )

            context = "\n".join(relevant_chunks)

            slide_content = self.llm.generate_slide(
                context=context,
                goal=goal
            )

            # Ensure slide_content is a Pydantic object
            if isinstance(slide_content, dict):
                slide_content = SlideContent(**slide_content)

            slides.append({
                "title": slide["title"],
                "content": "\n".join(slide_content.bullets),
                "visual": slide_content.visual,
                "metrics": slide_content.metrics or []
            })
            

        # -------------------------
        # 8. Format slides
        # -------------------------

        slides = self.formatter.format_slides(slides)

        return slides