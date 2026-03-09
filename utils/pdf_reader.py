import fitz  # PyMuPDF


class PDFReader:
    """
    Reads PDF files and extracts text content.
    """

    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path

    def extract_text(self) -> str:
        """
        Extract full text from the PDF.
        """

        document = fitz.open(self.pdf_path)

        pages_text = []

        for page_num in range(len(document)):
            page = document.load_page(page_num)

            text = page.get_text("text")

            if text:
                pages_text.append(text)

        document.close()

        return "\n".join(pages_text)