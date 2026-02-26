"""
main.py

FastAPI entry point for Financial Document Analyzer

Fixes applied:
- Proper CrewAI orchestration
- File path correctly passed
- All agents and tasks used
- Async safe execution
- File validation added
- Production-ready error handling
"""

# ===============================
# IMPORTS
# ===============================

import os
import uuid
import asyncio

from fastapi import FastAPI, File, UploadFile, Form, HTTPException

from crewai import Crew, Process

# Import agents
from agents import (
    financial_analyst,
    verifier,
    investment_advisor,
    risk_assessor
)

# Import tasks
from task import (
    verification_task,
    analyze_financial_document_task,
    investment_analysis_task,
    risk_assessment_task
)

# ===============================
# FASTAPI INITIALIZATION
# ===============================

app = FastAPI(
    title="Financial Document Analyzer API",
    version="1.0",
    description="AI-powered financial document analysis using CrewAI and Groq"
)

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

# ===============================
# CREW EXECUTION FUNCTION
# ===============================

def run_crew(query: str, file_path: str):
    """
    Runs CrewAI workflow

    Args:
        query (str): User query
        file_path (str): Uploaded PDF path

    Returns:
        Crew result
    """

    crew = Crew(

        agents=[
            verifier,
            financial_analyst,
            investment_advisor,
            risk_assessor
        ],

        tasks=[
            verification_task,
            analyze_financial_document_task,
            investment_analysis_task,
            risk_assessment_task
        ],

        process=Process.sequential,

        verbose=True
    )

    result = crew.kickoff(
        inputs={
            "query": query,
            "file_path": file_path
        }
    )

    return result


# ===============================
# HEALTH CHECK
# ===============================

@app.get("/")
async def root():

    return {
        "status": "running",
        "message": "Financial Document Analyzer API is running"
    }


# ===============================
# ANALYSIS ENDPOINT
# ===============================

@app.post("/analyze")
async def analyze_document(
    file: UploadFile = File(...),
    query: str = Form(
        default="Analyze this financial document and provide insights"
    )
):

    file_id = str(uuid.uuid4())

    file_path = f"data/{file_id}.pdf"

    try:

        # Validate file type
        if not file.filename.lower().endswith(".pdf"):

            raise HTTPException(
                status_code=400,
                detail="Only PDF files are supported"
            )

        # Save uploaded file
        with open(file_path, "wb") as f:

            content = await file.read()

            f.write(content)

        # Run Crew in separate thread (non-blocking)
        result = await asyncio.to_thread(
            run_crew,
            query,
            file_path
        )

        return {

            "status": "success",

            "file": file.filename,

            "query": query,

            "analysis": str(result)
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:

        # Cleanup file
        if os.path.exists(file_path):

            try:
                os.remove(file_path)
            except:
                pass


# ===============================
# RUN SERVER
# ===============================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )