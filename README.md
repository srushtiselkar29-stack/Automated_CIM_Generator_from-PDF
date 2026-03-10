# Automated CIM Generator from PDF

A Python-based solution to automatically generate **Confidential Information Memorandum (CIM)** presentations from PDF documents using AI.  
This project reads an annual report (PDF), extracts structured insights using AI models, plans slides, generates slide content, and outputs a PowerPoint presentation.

---

## Features

- Upload PDF reports via a **FastAPI endpoint**.
- Automatically extract structured insights:
  - Company overview
  - Products/Services
  - Market opportunity
  - Financial highlights
  - Competitive advantage
  - Risks
  - Growth strategy
- Plan slide structure for a 10-slide CIM deck.
- Generate structured slide content using AI.
- Output a ready-to-use PowerPoint (`.pptx`) presentation.
- Supports embedding models for semantic understanding.
- Keeps secrets secure using `.env` files.

---

## Folder Structure
Infosys/
├─ api/
│ └─ main.py # FastAPI server
├─ models/
│ ├─ document_analyzer.py # Extract insights from text
│ ├─ embedding_model.py # Text embeddings for semantic search
│ ├─ slide_generator.py # Generate structured slides
│ └─ slide_planner.py # Plan slide structure
├─ pipeline/
│ └─ report_pipeline.py # End-to-end report-to-PPT pipeline
├─ storage/
│ └─ generated_ppt/ # Output presentations (ignored in git)
├─ utils/ # Helper modules
├─ config/
│ └─ settings.py # Config (ignored in git, secrets kept in .env)
├─ .gitignore # Ignore venv, secrets, generated files
├─ requirements.txt # Python dependencies
└─ README.md


---

## Installation

1. Clone the repo:
git clone https://github.com/srushtiselkar29-stack/Automated_CIM_Generator_from-PDF.git
cd Automated_CIM_Generator_from-PDF

2. Create and activate a virtual environment:
   
macOS/Linux
python3 -m venv venv
source venv/bin/activate

Windows
python -m venv venv
venv\Scripts\activate

3. Install dependencies:
pip install -r requirements.txt

4. Add your Hugging Face token to a .env file:
HF_TOKEN=your_huggingface_token

---

## Usage
Run the API server
uvicorn api.main:app --reload

---

## Generate a PowerPoint from PDF

Send a POST request to /generate-ppt with a PDF file:
curl -X POST "http://127.0.0.1:8000/generate-ppt" \
  -F "file=@path_to_your_pdf.pdf"

Response:
JSON:
{
  "ppt_path": "path_to_generated_ppt.pptx"
}

---

## Notes

Keep all secrets (Hugging Face token, API keys) in .env.
The repo ignores:
  venv/
  .env
  config/settings.py
  storage/generated_ppt/
  *.ipynb and checkpoints

---

## Dependencies
Dependencies are listed in requirement.txt file

