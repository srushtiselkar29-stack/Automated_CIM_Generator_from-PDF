from fastapi import FastAPI, UploadFile, File
import shutil
from pathlib import Path

from pipeline.report_pipeline import ReportPipeline
from storage.ppt_generator import PPTGenerator


app = FastAPI()

UPLOAD_DIR = "uploads"
Path(UPLOAD_DIR).mkdir(exist_ok=True)


@app.post("/generate-ppt")
async def generate_ppt(file: UploadFile = File(...)):

    file_path = f"{UPLOAD_DIR}/{file.filename}"

    # Save uploaded PDF
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # -----------------------------
    # Run AI Report Pipeline
    # -----------------------------

    pipeline = ReportPipeline(file_path)

    slides = pipeline.run()

    # -----------------------------
    # Generate PowerPoint
    # -----------------------------

    ppt_generator = PPTGenerator()

    ppt_path = ppt_generator.create_presentation(
        title="Confidential Information Memorandum",
        slides=slides
    )

    return {"ppt_path": ppt_path}