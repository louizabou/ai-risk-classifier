"""
AI Risk Classifier — Azure AI Foundry
Author: Louiza Boujida | TheGovernAI.io
Description: Classifies an AI use case by regulatory risk level
             using GPT-4o mini + RAG on regulatory documents
             (EU AI Act, OSFI E-23, ISO 42001, Loi 25 QC)
"""

import os
from openai import AzureOpenAI

# ─────────────────────────────────────────────
# Configuration — use environment variables
# Never hardcode API keys directly in the code!
# ─────────────────────────────────────────────
AZURE_OPENAI_ENDPOINT = os.environ.get(
    "AZURE_OPENAI_ENDPOINT",
    "https://louiz-mmh5te2w-eastus2.openai.azure.com/openai/v1"
)
AZURE_OPENAI_API_KEY = os.environ.get("AZURE_OPENAI_API_KEY", "<your-api-key>")
DEPLOYMENT_NAME = "gpt-4o-mini-classifier"

# ─────────────────────────────────────────────
# System prompt v2 (versioned on GitHub)
# ─────────────────────────────────────────────
SYSTEM_PROMPT = """You are an AI Governance Risk Classifier. 
Your role is to analyze AI use cases submitted in natural language and classify them by risk level based on regulatory frameworks.

For each use case, you must:
1. Assign a risk level: MINIMAL, LIMITED, or HIGH
2. Reference the specific regulatory article that justifies the classification
3. List the required governance controls

Risk level definitions:
- MINIMAL: Internal operational tools with no impact on individuals
- LIMITED: Customer-facing or employee-facing systems requiring transparency and monitoring
- HIGH: Automated decisions affecting individuals' rights, employment, credit, or safety

Always ground your response in the indexed documents: EU AI Act, OSFI E-23, ISO 42001, or Loi 25 QC.
Always cite the specific article and document name.
Never introduce information not present in the source documents.
Be precise, structured, and concise."""


def classify_ai_use_case(use_case: str) -> dict:
    """
    Classifies an AI use case by regulatory risk level.

    Args:
        use_case (str): Use case description in natural language

    Returns:
        dict: {
            "use_case": str,
            "response": str,   # full model response
            "tokens_used": int
        }
    """
    # Initialize the Azure OpenAI client
    client = AzureOpenAI(
        azure_endpoint="https://louiz-mmh5te2w-eastus2.openai.azure.com",
        api_key=AZURE_OPENAI_API_KEY,
        api_version="2024-12-01-preview"
    )

    # Appel au modèle
    completion = client.chat.completions.create(
        model=DEPLOYMENT_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": use_case}
        ],
        max_tokens=800,
        temperature=0.1  # low temperature for consistent and deterministic responses
    )

    return {
        "use_case": use_case,
        "response": completion.choices[0].message.content,
        "tokens_used": completion.usage.total_tokens
    }


def main():
    """Sample classifications — the 4 POC use cases"""

    test_cases = [
        "We want to use AI to automatically approve or reject mortgage applications without human review.",
        "We want to use AI to automatically sort internal IT support tickets by priority level.",
        "We want to deploy an AI chatbot to answer general questions about our products.",
        "We want to use AI to analyze employee performance and decide promotions or terminations."
    ]

    print("=" * 60)
    print("AI RISK CLASSIFIER — TheGovernAI.io")
    print("=" * 60)

    for i, use_case in enumerate(test_cases, 1):
        print(f"\n📋 USE CASE {i}:")
        print(f"   {use_case}")
        print()

        result = classify_ai_use_case(use_case)

        print(f"🤖 CLASSIFICATION:")
        print(result["response"])
        print(f"\n📊 Tokens used: {result['tokens_used']}")
        print("-" * 60)


if __name__ == "__main__":
    main()
