#STEP 1 - EXTRACT TEXT FROM PDF

import pdfplumber

text = ""

with pdfplumber.open("infosys_report.pdf") as pdf:
    for page in pdf.pages:
        text += page.extract_text()

#STEP 2 - CHUNK THE DOCUMENT
print("STEP 2")
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500,
    chunk_overlap = 50
)

chunks = splitter.split_text(text)

#STEP 4 - CONVERT CHUNKS TO EMBEDDINGS
print("STEP 4")

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

embeddings = HuggingFaceEmbeddings(
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = FAISS.from_texts(chunks, embeddings)

#STEP 5 - BUILD RAG
print("step 5 llm rag")
query = query = """
Find information about Infosys including:
- Large Deal Total Contract Value (TCV)
- Revenue split by geography
- Infosys Topaz AI strategy
- Voluntary attrition rate trend
"""
docs = vectorstore.similarity_search(query)

#STEP 6 - USE LLM TO EXTRACT STRUCTURED INSIGHTS
print("STEP 6 - USE LLM TO EXTRACT STRUCTURED INSIGHTS")

from langchain_core.prompts import PromptTemplate
from transformers import pipeline

prompt_template = """
You are a financial analyst reading the Infosys annual report.

Extract the following information from the context:

1. Large Deal Total Contract Value (TCV)
2. Revenue split by geography
3. Key pillars of the Infosys Topaz AI strategy
4. Voluntary attrition rate trend over the last 4 quarters

If a value is not present, write "Not Found".

Context:
{context}

Return only valid JSON in this format:

{{
  "large_deal_tcv": "",
  "revenue_split": {{
      "North America": "",
      "Europe": "",
      "India": ""
  }},
  "topaz_strategy": [],
  "attrition_trend": []
}}
"""

print("STEP 6: Building prompt...")

prompt = PromptTemplate(
    template=prompt_template,
    input_variables=["context"]
)

query = "Infosys large deal TCV revenue split attrition trend Topaz strategy"

docs = vectorstore.similarity_search(query, k=2)

context = "\n".join([doc.page_content for doc in docs])
context = context[:1200]

final_prompt = prompt.format(context=context)

print("Loading LLM model...")
# Local LLM
llm = pipeline(
    "text2text-generation",
    model="",
    truncation = True
)

print("Model loaded. Generating response...")
response = llm(final_prompt, max_new_tokens = 300, do_sample = False)

print(response[0]["generated_text"])