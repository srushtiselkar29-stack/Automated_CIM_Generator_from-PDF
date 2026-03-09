from typing import List
import re


class TextChunker:
    """
    Splits text into semantic chunks using paragraphs
    and keeps context overlap.
    """

    def __init__(self, chunk_size: int = 1000, overlap: int = 150):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def split_text(self, text: str) -> List[str]:

        # Split by paragraph first
        paragraphs = re.split(r"\n\s*\n", text)

        chunks = []
        current_chunk = ""

        for para in paragraphs:

            if len(current_chunk) + len(para) < self.chunk_size:
                current_chunk += para + "\n"

            else:
                chunks.append(current_chunk.strip())

                # overlap
                current_chunk = current_chunk[-self.overlap:] + para + "\n"

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks