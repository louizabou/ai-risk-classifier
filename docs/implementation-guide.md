# 🛡️ AI Risk Classifier — Complete Implementation Guide

**A GenAIOps POC Built on Azure AI Foundry**

> Author: Louiza Boujida | [TheGovernAI.io](https://thegovernai.io)  
> Version: 1.0 | March 2026  
> License: MIT

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [System Architecture](#2-system-architecture)
3. [Phase 1 — Azure Infrastructure Setup](#3-phase-1--azure-infrastructure-setup)
4. [Phase 2 — RAG Pipeline Configuration](#4-phase-2--rag-pipeline-configuration)
5. [Phase 3 — Testing & Evaluation](#5-phase-3--testing--evaluation)
6. [Phase 4 — API Integration](#6-phase-4--api-integration)
7. [System Prompts (Versioned)](#7-system-prompts-versioned)
8. [Repository Structure](#8-repository-structure)
9. [Known Limitations & Roadmap](#9-known-limitations--roadmap)
10. [Cost Estimate](#10-cost-estimate)
11. [Glossary](#11-glossary)

---

## 1. Executive Summary

This guide is a complete, step-by-step implementation reference for the **AI Risk Classifier** — a GenAIOps proof of concept built on Microsoft Azure AI Foundry.

It demonstrates how to operationalize a pre-trained language model with:
- **Retrieval-Augmented Generation (RAG)** over regulatory documents
- **Automated evaluation** with measurable quality metrics
- **Prompt versioning** on GitHub
- **API-ready Python client** for enterprise integration

> 💡 **The core problem solved:** In regulated industries, evaluating whether an AI use case is HIGH, LIMITED, or MINIMAL risk under the EU AI Act, OSFI E-23, ISO 42001, and Loi 25 QC can take weeks manually. This system does it in seconds.

### AI-300 Domain Coverage

| Domain | Coverage |
|--------|----------|
| Domain 1 — MLOps Infrastructure | GitHub repo, Azure resource provisioning |
| Domain 3 — GenAIOps Infrastructure | Azure AI Foundry, serverless model, prompt versioning |
| Domain 4 — GenAI QA & Observability | Automated evaluation, Groundedness, Relevance metrics |
| Domain 5 — RAG Optimization | Azure AI Search index, keyword retrieval, document chunking |

### Tech Stack

| Component | Details |
|-----------|---------|
| Platform | Azure AI Foundry (Hub + Project) |
| Model | GPT-4o mini — Standard tier, East US 2 |
| Search | Azure AI Search — Basic tier, Keyword search |
| Regulatory Docs | EU AI Act, OSFI E-23, ISO 42001, Loi 25 QC |
| Language | Python 3.10+ / OpenAI SDK |
| Repository | GitHub — Public |

---

## 2. System Architecture

### How It Works

1. User submits an AI use case in plain natural language
2. Azure AI Search retrieves relevant passages from regulatory PDFs (RAG)
3. GPT-4o mini classifies the use case with regulatory justification and governance controls

> **WHY RAG?** A standalone LLM can hallucinate regulatory articles. By grounding responses in real indexed documents, every classification cites verifiable sources.

### Architecture Diagram

```
User Input (natural language)
        │
        ▼
Azure AI Search ◄── eu-ai-act-2024.pdf
(regulatory-docs-index) ◄── osfi-e23-model-risk-2027.pdf
                        ◄── iso-42001-ai-management-2023.pdf
                        ◄── loi25-quebec-privacy.pdf
        │
        ▼
GPT-4o mini (gpt-4o-mini-classifier)
+ System Prompt v2 (versioned on GitHub)
        │
        ▼
Risk Classification + Regulatory Citation + Governance Controls
        │
   ┌────┴────┐
   ▼         ▼
Evaluation  Tracing
(Foundry)  (App Insights)
```

### Regulatory Documents Indexed

| Document | Source | Purpose |
|----------|--------|---------|
| EU AI Act 2024 | Official EU Journal | Risk classification, prohibited practices (Art. 5, 6) |
| OSFI E-23 Model Risk | Office of the Superintendent of Financial Institutions | Model validation, human oversight requirements |
| ISO 42001:2023 | International Organization for Standardization | AI management system framework |
| Loi 25 QC | Gouvernement du Québec | Personal data protection, automated decision disclosure |

---

## 3. Phase 1 — Azure Infrastructure Setup

> **WHY this phase?** Every GenAI system needs a governed, secure cloud infrastructure. Azure AI Foundry provides a centralized hub that connects the model, search index, monitoring, and evaluation in one auditable workspace.

### Step 1.1 — Create Azure Resource Group

A Resource Group is a logical container for all Azure resources associated with this project.

1. In Azure Portal, navigate to **Resource Groups**
2. Click **Create**
3. Configure:
   - **Subscription:** Your Azure subscription
   - **Resource Group Name:** `rg-ai-risk-classifier`
   - **Region:** Canada Central
4. Click **Review + Create** → **Create**

### Step 1.2 — Create Azure AI Foundry Hub

The Hub is the top-level workspace managing shared infrastructure (storage, Key Vault, networking).

1. In Azure Portal, search for **Azure AI Foundry**
2. Click **Create > New hub**
3. Configure:
   - **Hub Name:** `hub-ai-risk-classifier`
   - **Region:** Canada Central
   - **Resource Group:** `rg-ai-risk-classifier`
4. Click **Create** and wait ~3 minutes

> ⚠️ **Region limitation:** Canada Central does not support GlobalStandard SKU for model deployments. Use Standard tier and deploy the model in **East US 2** instead.

### Step 1.3 — Create Azure AI Foundry Project

1. Inside the Hub, click **+ New Project**
2. **Name:** `ai-risk-classifier`
3. Click **Create**

### Step 1.4 — Deploy GPT-4o Mini

GPT-4o mini processes the user query combined with regulatory document chunks and generates the structured classification.

1. Navigate to **Model catalog**
2. Search for `gpt-4o-mini` and click **Deploy**
3. Configure:
   - **Deployment name:** `gpt-4o-mini-classifier`
   - **Deployment type:** Standard
   - **Region:** East US 2 *(required for Standard tier)*
4. Click **Deploy**

### Step 1.5 — Create Azure AI Search

Azure AI Search stores chunked regulatory documents and returns relevant passages at query time.

1. In Azure Portal, search for **Azure AI Search**
2. Click **Create**
3. Configure:
   - **Service name:** `searchairisklclassifier`
   - **Region:** Canada Central
   - **Pricing tier:** Basic (~$8 USD/month)
4. Click **Review + Create** → **Create**

> **NOTE:** Vector embeddings (text-embedding-ada-002) are not supported in Canada Central. This project uses keyword search, which is sufficient for regulatory document retrieval.

---

## 4. Phase 2 — RAG Pipeline Configuration

> **WHY RAG?** Without RAG, the LLM answers from training data only — which may be outdated or hallucinated for specific regulatory articles. RAG grounds every response in your actual indexed documents.

### Step 2.1 — Prepare Regulatory Documents

Download and store locally:

| File | Description | Size |
|------|-------------|------|
| `eu-ai-act-2024.pdf` | EU AI Act — Official Journal of the EU | 2.46 MB |
| `osfi-e23-model-risk-2027.pdf` | OSFI E-23 Model Risk Management | 123 KB |
| `iso-42001-ai-management-2023.pdf` | ISO 42001 AI Management System | 81 KB |
| `loi25-quebec-privacy.pdf` | Loi 25 — Quebec Privacy Law | 255 KB |

### Step 2.2 — Configure the Chat Playground

1. Navigate to **Playgrounds > Chat playground**
2. Select deployment: `gpt-4o-mini-classifier`
3. In the **System Prompt** field, paste the [System Prompt v2](#72-v2-prompttxt--improved)
4. Click **Add your data (PREVIEW)**
5. Select **Azure AI Search** and configure:
   - **Index name:** `regulatory-docs-index`
   - **Search type:** Keyword
6. Upload all 4 regulatory PDFs and wait for indexation

The indexation pipeline completes 3 steps:
- **Cracking & Chunking** — PDFs split into text chunks
- **Creating AI Search Index** — Schema registered in Azure AI Search
- **Indexation** — Chunks stored and made searchable

---

## 5. Phase 3 — Testing & Evaluation

### Step 3.1 — Manual Testing (4 Use Cases)

> **WHY test manually first?** Manual testing validates system logic before automating evaluation. It confirms the RAG pipeline retrieves relevant documents and the model produces accurate classifications.

| # | Use Case | Expected | Result |
|---|----------|----------|--------|
| 1 | AI to auto-approve/reject mortgage applications without human review | HIGH | HIGH ✅ |
| 2 | AI to sort internal IT support tickets by priority level | LIMITED | LIMITED ✅ |
| 3 | AI chatbot to answer general product/service questions | LIMITED | LIMITED ✅ |
| 4 | AI to decide employee promotions and terminations | HIGH | HIGH ✅ |

All 4 tests passed with correct risk classification and regulatory citations (EU AI Act Article 5, OSFI E-23, Loi 25 QC).

### Step 3.2 — Prompt Versioning on GitHub

Prompt versioning is a core GenAIOps practice. Every change to the system prompt is tracked as a new version.

1. Create `prompts/v1-prompt.txt` → commit `Create v1-prompt`
2. Create `prompts/v2-prompt.txt` → commit `Create v2-prompt`

GitHub maintains the full history — enabling rollback, comparison, and audit trail.

### Step 3.3 — Automated Evaluation

> **WHY automated evaluation?** Manual testing proves the system works today. Automated evaluation proves it works consistently across all inputs, with measurable quality metrics trackable over time.

#### Evaluation Progression

| Run | Dataset | Prompt | Groundedness | Relevance |
|-----|---------|--------|-------------|-----------|
| eval-v1 | test-cases.jsonl (no context) | v1 | 🟡 75% (3/4) | 🟢 100% (4/4) |
| eval-v2 | test-cases.jsonl (no context) | v2 | 🔴 50% (2/4) | 🟢 100% (4/4) |
| eval-v3 | test-cases-v2.jsonl (with context) | v2 | 🟢 **100% (4/4)** | 🟢 **100% (4/4)** |

> 💡 **Key insight:** The progression 75% → 50% → 100% is not a failure — it is the **GenAIOps workflow in action**: Measure → Identify → Improve → Validate. This is exactly what AI-300 Domain 4 evaluates.

#### Why Groundedness Improved

The Groundedness score measures how well the model response is anchored in source documents. The jump to 100% was achieved by adding a `context` column to the evaluation dataset — providing the evaluator with actual regulatory article excerpts to compare against.

#### Evaluation Dataset Format (JSONL)

```jsonl
{"query": "We want to use AI to automatically approve mortgage applications without human review.", "expected_response": "HIGH", "context": "EU AI Act Article 5 prohibits AI systems that make automated decisions affecting individuals access to credit without human oversight. OSFI E-23 requires model validation and human review for credit decisions."}
```

#### Evaluation Metrics

| Metric | What It Measures | Target |
|--------|-----------------|--------|
| Groundedness | Is the response anchored in the indexed documents? | >= 80% |
| Relevance | Does the response address the question asked? | >= 90% |

---

## 6. Phase 4 — API Integration

> **WHY build an API client?** A Playground demo proves the concept. An API client proves production readiness — enabling integration into governance portals, intake forms, Slack bots, or any enterprise system.

### Prerequisites

- Python 3.10+
- `pip3 install openai`
- Azure API Key from **Foundry > Playground > View code**

### Environment Configuration

Never hardcode API keys in source code. Use environment variables:

```bash
export AZURE_OPENAI_API_KEY="YOUR-API-KEY"
```

> 🔒 **Security best practice:** In production, store secrets in Azure Key Vault or GitHub Secrets. Never commit API keys to version control.

### Running the Script

```bash
git clone https://github.com/louIzabou/ai-risk-classifier
cd ai-risk-classifier
pip3 install openai
export AZURE_OPENAI_API_KEY="YOUR-API-KEY"
python3 src/classifier.py
```

### Expected Output

```
============================================================
AI RISK CLASSIFIER — TheGovernAI.io
============================================================

📋 USE CASE 1:
   We want to use AI to automatically approve or reject
   mortgage applications without human review.

🤖 CLASSIFICATION:
1. **Risk Level**: HIGH
2. **Regulatory Article**: Article 5 of the EU AI Act...
3. **Required Governance Controls**:
   - Conduct a risk assessment...
   - Implement transparency measures...
   - Establish a human oversight mechanism...

📊 Tokens used: 318
```

---

## 7. System Prompts (Versioned)

> **WHY version prompts?** The system prompt is the instruction layer of the AI. Like code, it must be versioned, tested, and reviewed. Prompt versioning enables rollback, A/B comparison, and audit trail.

### 7.1 v1-prompt.txt — Baseline

```
You are an AI Governance Risk Classifier.
Your role is to analyze AI use cases submitted in natural language
and classify them by risk level based on regulatory frameworks.

For each use case, you must:
1. Assign a risk level: MINIMAL, LIMITED, or HIGH
2. Reference the specific regulatory article that justifies
   the classification
3. List the required governance controls

Always cite: EU AI Act, OSFI E-23, ISO 42001, or Loi 25 QC
when relevant. Be precise, structured, and concise.
```

### 7.2 v2-prompt.txt — Improved

**Changes from v1:** Added explicit risk level definitions and grounding instructions to fix Groundedness score.

```
You are an AI Governance Risk Classifier.
Your role is to analyze AI use cases submitted in natural language
and classify them by risk level based on regulatory frameworks.

For each use case, you must:
1. Assign a risk level: MINIMAL, LIMITED, or HIGH
2. Reference the specific regulatory article that justifies
   the classification
3. List the required governance controls

Risk level definitions:
- MINIMAL: Internal operational tools with no impact on individuals
- LIMITED: Customer-facing or employee-facing systems requiring
  transparency and monitoring
- HIGH: Automated decisions affecting individuals' rights,
  employment, credit, or safety

Always ground your response in the indexed documents:
EU AI Act, OSFI E-23, ISO 42001, or Loi 25 QC.
Always cite the specific article and document name.
Never introduce information not present in the source documents.
Be precise, structured, and concise.
```

---

## 8. Repository Structure

```
ai-risk-classifier/
├── README.md                  # Project overview, badges, architecture
├── .gitignore                 # Excludes API keys, venv, __pycache__
├── LICENSE                    # MIT License
├── prompts/
│   ├── v1-prompt.txt          # Baseline system prompt
│   └── v2-prompt.txt          # Improved system prompt
├── src/
│   └── classifier.py          # Python API client
└── data/
    ├── test-cases.jsonl        # Evaluation dataset v1 (no context)
    └── test-cases-v2.jsonl     # Evaluation dataset v2 (with context)
```

> **Note:** Regulatory PDFs are stored locally and NOT committed to GitHub (licensing restrictions). Only the evaluation datasets are versioned.

---

## 9. Known Limitations & Roadmap

| Limitation | Impact | Recommended Solution |
|-----------|--------|---------------------|
| Regulatory PDFs may become outdated | Classifier cites obsolete articles | Implement automated monitoring of source URLs + scheduled re-indexing (Azure Logic Apps or ADF) |
| Keyword search only | Lower retrieval precision for semantic queries | Migrate to vector embeddings once supported in Canada Central |
| No RAG in API client | API calls bypass indexed documents | Integrate Azure AI Search SDK into classifier.py |
| Tracing requires instrumentation | Playground calls not traced in App Insights | Add OpenTelemetry to classifier.py |
| Single region | Canada Central limitations | Evaluate multi-region deployment for production |

---

## 10. Cost Estimate

| Resource | Tier | Est. Monthly Cost (USD) |
|----------|------|------------------------|
| Azure AI Search | Basic | ~$8.00 |
| GPT-4o mini | Pay-per-token (Standard) | ~$3–8 (POC usage) |
| Azure Storage (Foundry) | LRS — included | <$1.00 |
| Application Insights | Pay-per-use | <$1.00 |
| **Total** | | **~$12–18 / month** |

---

## 11. Glossary

| Term | Definition |
|------|-----------|
| **RAG** | Retrieval-Augmented Generation — architecture where a search index retrieves relevant document chunks at query time, passed as context to the LLM to reduce hallucinations. |
| **Groundedness** | Evaluation metric measuring how well an LLM response is anchored in provided source documents. 100% = all claims traceable to indexed content. |
| **GenAIOps** | Operational practices for deploying, monitoring, evaluating, and iterating on generative AI systems built on pre-trained foundation models. |
| **System Prompt** | Instructions given to an LLM before user input. Defines role, behavior, output format, and constraints. |
| **Prompt Versioning** | Practice of storing each system prompt iteration in version control with a unique version identifier — enabling rollback and audit trail. |
| **Azure AI Foundry** | Microsoft's unified platform for building, deploying, and managing generative AI applications. |
| **OSFI E-23** | Office of the Superintendent of Financial Institutions Guideline E-23 — Model Risk Management for Canadian federally regulated financial institutions. |
| **EU AI Act** | Regulation (EU) 2024/1689 — The world's first comprehensive AI legal framework, classifying AI systems by risk level. |

---

## Document Information

| Field | Value |
|-------|-------|
| Author | Louiza Boujida |
| Brand | TheGovernAI.io |
| Version | 1.0 |
| Date | March 2026 |
| License | MIT — Free to use with attribution |
| GitHub | github.com/louIzabou/ai-risk-classifier |

---

> ⚠️ All Azure resource names, endpoints, and API keys shown in this guide use placeholder values. Never expose real credentials in documentation.
