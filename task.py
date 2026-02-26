"""
task.py

Defines all CrewAI tasks for financial document analysis.

Fixes applied:
- Removed hallucination instructions
- Proper agents assigned
- Proper task descriptions
- Production-ready workflow
- Structured output
"""

# ===============================
# IMPORTS
# ===============================

from crewai import Task

from agents import (
    financial_analyst,
    verifier,
    investment_advisor,
    risk_assessor
)

from tools import FinancialDocumentTool


# ===============================
# DOCUMENT VERIFICATION TASK
# ===============================

verification_task = Task(

    description=(
        "Verify that the provided file is a valid financial document.\n"
        "Extract key financial sections such as revenue, profit, expenses, "
        "assets, liabilities, and financial summaries.\n\n"
        "File path: {file_path}"
    ),

    expected_output=(
        "Confirmation whether document is valid financial document.\n"
        "Summary of document type.\n"
        "Key financial sections identified."
    ),

    agent=verifier,

    tools=[
        FinancialDocumentTool.read_data_tool
    ],

    async_execution=False,
)

# ===============================
# FINANCIAL ANALYSIS TASK
# ===============================

analyze_financial_document_task = Task(

    description=(
        "Analyze the financial document at {file_path}.\n"
        "User query: {query}\n\n"
        "Extract and analyze:\n"
        "- Revenue\n"
        "- Net profit\n"
        "- Expenses\n"
        "- Growth indicators\n"
        "- Financial performance\n\n"
        "Provide clear financial insights."
    ),

    expected_output=(
        "Detailed financial analysis including:\n"
        "- Revenue analysis\n"
        "- Profitability analysis\n"
        "- Financial health summary\n"
        "- Key insights"
    ),

    agent=financial_analyst,

    tools=[
        FinancialDocumentTool.read_data_tool
    ],

    async_execution=False,
)

# ===============================
# INVESTMENT ANALYSIS TASK
# ===============================

investment_analysis_task = Task(

    description=(
        "Based on financial document at {file_path}, provide investment analysis.\n\n"
        "Include:\n"
        "- Investment potential\n"
        "- Strengths\n"
        "- Weaknesses\n"
        "- Recommendation (Buy, Hold, Sell)\n"
    ),

    expected_output=(
        "Professional investment recommendation including:\n"
        "- Investment rating\n"
        "- Justification\n"
        "- Supporting financial metrics"
    ),

    agent=investment_advisor,

    tools=[
        FinancialDocumentTool.read_data_tool
    ],

    async_execution=False,
)

# ===============================
# RISK ASSESSMENT TASK
# ===============================

risk_assessment_task = Task(

    description=(
        "Perform risk assessment of financial document at {file_path}.\n\n"
        "Identify:\n"
        "- Financial risks\n"
        "- Liquidity risks\n"
        "- Profitability risks\n"
        "- Operational risks"
    ),

    expected_output=(
        "Detailed risk assessment including:\n"
        "- Risk level (Low, Medium, High)\n"
        "- Risk factors\n"
        "- Risk mitigation suggestions"
    ),

    agent=risk_assessor,

    tools=[
        FinancialDocumentTool.read_data_tool
    ],

    async_execution=False,
)