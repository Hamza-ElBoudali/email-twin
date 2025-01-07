from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import openai
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
import os

load_dotenv()  # Load environment variables from .env file

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")

class EmailThread(BaseModel):
    messages: List[dict]
    pdf_contents: Optional[List[str]] = None
    user_id: str

class StyleAnalysisRequest(BaseModel):
    email_samples: List[str]
    user_id: str

@app.post("/analyze-style")
async def analyze_writing_style(request: StyleAnalysisRequest):
    try:
        prompt = f"""Analyze the following email samples and learn the writing style:
        {'\n'.join(request.email_samples)}
        
        Provide a detailed description of the writing style characteristics."""
        
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": prompt}]
        )
        
        # Store the style analysis in a database for future use
        # ... (implement database storage logic)
        
        return {"status": "success", "style_analysis": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-response")
async def generate_email_response(thread: EmailThread):
    try:
        # Create vector store from PDF contents if available
        relevant_context = ""
        if thread.pdf_contents:
            embeddings = OpenAIEmbeddings()
            vectorstore = Chroma.from_texts(thread.pdf_contents, embeddings)
            
            # Get relevant chunks based on the latest email
            latest_email = thread.messages[-1]["content"]
            relevant_docs = vectorstore.similarity_search(latest_email, k=3)
            relevant_context = "\n".join([doc.page_content for doc in relevant_docs])
        
        # Retrieve stored style analysis
        # ... (implement database retrieval logic)
        
        prompt = f"""Based on the following email thread and context, generate a response that matches the user's writing style:
        
        Thread:
        {thread.messages}
        
        Relevant PDF Context:
        {relevant_context}
        
        Generate a response email, using the thread and pdf content as context, that maintains the user's writing style."""
        
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": prompt}]
        )
        
        return {"response": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))