# ai-risk-classifier
# 🛡️ AI Risk Classifier

> **A GenAIOps POC built on Azure AI Foundry** — Classify AI use cases by risk level using RAG over EU AI Act, OSFI B-13, ISO 42001, and Loi 25 QC.

[![Azure AI Foundry](https://img.shields.io/badge/Azure-AI%20Foundry-0078D4?logo=microsoft-azure)](https://ai.azure.com)
[![Model](https://img.shields.io/badge/Model-GPT--4o--mini-412991?logo=openai)](https://azure.microsoft.com)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Author](https://img.shields.io/badge/Author-TheGovernAI.io-blueviolet)](https://thegovernai.io)

---

## 🎯 What It Does

Submit any AI use case in plain language — get an instant risk classification with regulatory justification and recommended governance controls.

**Example input:**
> *"We want to use AI to automatically score SME credit applications without human review."*

**Example output:**
```
⚠️  RISK LEVEL: HIGH

EU AI Act   → Article 6 — High-risk system (credit scoring)
OSFI B-13   → Section 4.2 — Automated decisions with financial impact
ISO 42001   → Clause 6.1.2 — Risk treatment required

Recommended Controls:
  ✅ Human-in-the-loop mandatory
  ✅ Model explainability (XAI)
  ✅ Complete audit trail
  ✅ Chief Risk Officer validation
```

---

## 🏗️ Architecture

```
User Input (natural language)
        │
        ▼
Azure AI Search ──── EU AI Act (PDF)
  (RAG Index)    ──── OSFI B-13 (PDF)
                 ──── ISO 42001 (PDF)
                 ──── Loi 25 QC (PDF)
        │
        ▼
GPT-4o mini (serverless)
+ Versioned Prompt (Git)
        │
        ▼
Risk Classification + Justification
        │
        ▼
Auto-Evaluation          Observability
(Groundedness,           (Latency, Tokens,
 Relevance,               Cost tracking)
 Coherence)
```

---

## 📋 Regulatory Framework Coverage

| Framework | Scope | Why It Matters |
|---|---|---|
| **EU AI Act** | Global standard | Risk classification tiers |
| **OSFI B-13** | Canadian banks | Technology & AI risk guideline |
| **ISO 42001** | International | AI Management System standard |
| **Loi 25 QC** | Quebec | Privacy & automated decisions |

---

## 🔧 Tech Stack

| Component | Technology |
|---|---|
| AI Platform | Azure AI Foundry |
| LLM | GPT-4o mini (serverless) |
| Search | Azure AI Search (RAG) |
| IaC | Bicep + Azure CLI |
| CI/CD | GitHub Actions |
| Evaluation | Azure AI Evaluation SDK |
| Observability | Azure AI Foundry Tracing |

---

## 📁 Project Structure

```
ai-risk-classifier/
├── README.md
├── .gitignore
├── requirements.txt
├── infra/
│   ├── main.bicep              # Infrastructure as Code
│   ├── parameters.dev.json     # Dev environment parameters
│   ├── parameters.prod.json    # Prod environment parameters (dry run)
│   └── README.md               # Infra deployment guide
├── data/
│   └── test-cases.json         # 20 evaluation test cases
├── prompts/
│   ├── v1-prompt.txt           # Initial prompt
│   ├── v2-prompt.txt           # Optimized variant
│   └── v3-prompt.txt           # Final production prompt
├── src/
│   └── classifier.py           # Main classification logic
└── docs/
    ├── architecture.md         # Architecture diagram
    └── evaluation-results.md   # Evaluation metrics
```

---

## 🚀 Getting Started

### Prerequisites
- Azure subscription
- Azure AI Foundry project
- Azure AI Search service
- Python 3.10+
- ### Deploy Infrastructure
```bash
# Validate (dry run)
az deployment group validate \
  --resource-group <your-rg> \
  --template-file infra/main.bicep \
  --parameters infra/parameters.dev.json

# Deploy Dev
az deployment group create \
  --resource-group <your-rg> \
  --template-file infra/main.bicep \
  --parameters infra/parameters.dev.json \
  --name bicep-deploy-dev
```

### Setup

```bash
# Clone the repo
git clone https://github.com/louIzabou/ai-risk-classifier.git
cd ai-risk-classifier

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env
# Fill in your Azure credentials in .env
```

---

## 📊 GenAIOps Coverage (AI-300 Alignment)

This POC demonstrates the following AI-300 exam domains:

| Domain | Coverage |
|---|---|
| IaC & IAM (15-20%) | Bicep template, RBAC configuration |
| GenAIOps Infrastructure (20-25%) | Foundry project, serverless endpoint, prompt versioning |
| QA & Observability (10-15%) | Groundedness, relevance, coherence metrics |
| RAG Optimization (10-15%) | Chunking strategy, hybrid search, A/B prompt testing |

---

## ✍️ Author

**Louiza Boujida** — AI & Advanced Analytics Architect  
🌐 [TheGovernAI.io](https://thegovernai.io) · 💼 [LinkedIn](https://linkedin.com/in/louizaboujida) · ✍️ [Medium](https://medium.com/@louizabou)

*This project is part of a hands-on preparation for the Microsoft AI-300 certification.*

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.
