"""
agents.py

This file defines all CrewAI agents used in the Financial Document Analyzer system.

Fixes applied:
- Proper Groq LLM initialization
- Fixed tools parameter
- Correct agent goals
- Added environment validation
- Production-ready configuration
"""

# ===============================
# IMPORTS
# ===============================

import os
from dotenv import load_dotenv

from crewai import Agent, LLM

from tools import FinancialDocumentTool
from crewai import LLM
import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# Load environment variables
load_dotenv()

# ===============================
# VALIDATE GROQ API KEY
# ===============================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found in environment variables. "
        "Please add it to your .env file"
    )

# ===============================
# INITIALIZE GROQ LLM
# ===============================
# CrewAI supports Groq using OpenAI-compatible format

llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
    temperature=0.2
)

# ===============================
# FINANCIAL ANALYST AGENT
# ===============================

financial_analyst = Agent(
    role="Senior Financial Analyst",

    goal=(
        "Analyze financial documents thoroughly and provide accurate financial insights, "
        "investment recommendations, and key financial metrics based on real document data."
    ),

    backstory=(
        "You are an experienced financial analyst with deep expertise in reading "
        "financial statements, annual reports, balance sheets, and income statements. "
        "You provide data-driven insights and professional financial analysis."
    ),

    verbose=True,

    memory=True,

    tools=[
        FinancialDocumentTool.read_data_tool
    ],

    llm=llm,

    allow_delegation=False,

    max_iter=3,

    max_rpm=10
)

# ===============================
# DOCUMENT VERIFIER AGENT
# ===============================

verifier = Agent(
    role="Financial Document Verification Specialist",

    goal=(
        "Verify whether the uploaded file is a valid financial document "
        "and extract relevant financial information safely."
    ),

    backstory=(
        "You specialize in verifying financial documents including earnings reports, "
        "financial statements, and investment reports. You ensure document authenticity."
    ),

    verbose=True,

    memory=True,

    tools=[
        FinancialDocumentTool.read_data_tool
    ],

    llm=llm,

    allow_delegation=False,

    max_iter=2,

    max_rpm=10
)

# ===============================
# INVESTMENT ADVISOR AGENT
# ===============================

investment_advisor = Agent(
    role="Investment Advisor",

    goal=(
        "Provide investment recommendations based strictly on financial document analysis "
        "and real financial indicators."
    ),

    backstory=(
        "You are a certified investment advisor who helps investors make informed "
        "decisions based on financial reports and company performance."
    ),

    verbose=True,

    memory=True,

    tools=[
        FinancialDocumentTool.read_data_tool
    ],

    llm=llm,

    allow_delegation=False,

    max_iter=3,

    max_rpm=10
)

# ===============================
# RISK ASSESSMENT AGENT
# ===============================

risk_assessor = Agent(
    role="Financial Risk Assessment Expert",

    goal=(
        "Identify financial risks, company weaknesses, and potential investment risks "
        "based on financial document analysis."
    ),

    backstory=(
        "You specialize in identifying financial risks such as liquidity risk, "
        "market risk, operational risk, and financial instability."
    ),

    verbose=True,

    memory=True,

    tools=[
        FinancialDocumentTool.read_data_tool
    ],

    llm=llm,

    allow_delegation=False,

    max_iter=3,

    max_rpm=10
)