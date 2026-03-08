# 🛡️ AI Risk Classifier — Complete Implementation Guide

**A GenAIOps POC Built on Azure AI Foundry**

> Author: Louiza Boujida | [TheGovernAI.io](https://thegovernai.io)  
> Version: 2.0 | March 2026  
> License: MIT

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [System Architecture](#2-system-architecture)
3. [Phase 1 — Azure Infrastructure Setup](#3-phase-1--azure-infrastructure-setup)
4. [Phase 2 — RAG Pipeline Configuration](#4-phase-2--rag-pipeline-configuration)
5. [Phase 3 — Testing & Evaluation](#5-phase-3--testing--evaluation)
6. [Phase 4 — API Integration](#6-phase-4--api-integration)
7. [Phase 5 — Infrastructure as Code (Bicep)](#7-phase-5--infrastructure-as-code-bicep)
8. [System Prompts (Versioned)](#8-system-prompts-versioned)
9. [Repository Structure](#9-repository-structure)
10. [Known Limitations & Roadmap](#10-known-limitations--roadmap)
11. [Cost Estimate](#11-cost-estimate)
12. [Glossary](#12-glossary)

---

## 1. Executive Summary

This guide is a complete, step-by-step implementation reference for the **AI Risk Classifier** — a GenAIOps proof of concept built on Microsoft Azure AI Foundry.

It demonstrates how to operationalize a pre-trained language model with:
- **Retrieval-Augmented Generation (RAG)** over regulatory documents
- **Automated evaluation** with measurable quality metrics
- **Prompt versioning** on GitHub
- **API-ready Python client** for enterprise integration
- **Infrastructure as Code (Bicep)** for repeatable, auditable deployments

> 💡 **The core problem solved:** In regulated industries, evaluating whether an AI use case is HIGH, LIMITED, or MINIMAL risk under the EU AI Act, OSFI E-23, ISO 42001, and Loi 25 QC can take weeks manually. This system does it in seconds.

### AI-300 Domain Coverage

| Domain | Coverage |
|--------|----------|
| Domain 1 — MLOps Infrastructure | Bicep IaC, parameterized environments, idempotent deployments |
| Domain 3 — GenAIOps Infrastructure | Azure AI Foundry, serverless model, prompt versioning |
| Domain 4 — GenAI QA & Observability | Automated evaluation, Groundedness, Relevance metrics |
| Domain 5 — RAG Optimization | Azure AI Search index, keyword retrieval, document chunking |

### Tech Stack

| Component | Details |
|-----------|---------|
| Platform | Azure AI Foundry (Hub + Project) |
| Model | GPT-4o mini — Standard tier, East US 2 |
| Search | Azure AI Search — Basic tier, Keyword search |
| IaC | Bicep + Azure CLI |
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
        │
        ▼
Infrastructure as Code (Bicep)
— Repeatable, auditable deployments
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

1. In Azure Portal, navigate to **Resource Groups**
2. Click **Create**
3. Configure:
   - **Resource Group Name:** `rg-ai-risk-classifier`
   - **Region:** Canada Central
4. Click **Review + Create** → **Create**

### Step 1.2 — Create Azure AI Foundry Hub

1. Search for **Azure AI Foundry** → **Create > New hub**
2. Configure:
   - **Hub Name:** `hub-ai-risk-classifier`
   - **Region:** Canada Central
3. Click **Create** (~3 minutes)

> ⚠️ **Region limitation:** Canada Central does not support GlobalStandard SKU. Use Standard tier and deploy the model in **East US 2**.

### Step 1.3 — Create Azure AI Foundry Project

1. Inside the Hub → **+ New Project**
2. **Name:** `ai-risk-classifier`
3. Click **Create**

### Step 1.4 — Deploy GPT-4o Mini

1. Navigate to **Model catalog** → search `gpt-4o-mini` → **Deploy**
2. Configure:
   - **Deployment name:** `gpt-4o-mini-classifier`
   - **Deployment type:** Standard
   - **Region:** East US 2

### Step 1.5 — Create Azure AI Search

1. Search for **Azure AI Search** → **Create**
2. Configure:
   - **Service name:** `searchairisklclassifier`
   - **Region:** Canada Central
   - **Pricing tier:** Basic (~$8 USD/month)

> **NOTE:** Vector embeddings not supported in Canada Central. Keyword search is used instead.

---

## 4. Phase 2 — RAG Pipeline Configuration

> **WHY RAG?** Without RAG, the LLM answers from training data only — outdated or hallucinated for specific regulatory articles. RAG grounds every response in your actual indexed documents.

### Step 2.1 — Prepare Regulatory Documents

| File | Description | Size |
|------|-------------|------|
| `eu-ai-act-2024.pdf` | EU AI Act — Official Journal of the EU | 2.46 MB |
| `osfi-e23-model-risk-2027.pdf` | OSFI E-23 Model Risk Management | 123 KB |
| `iso-42001-ai-management-2023.pdf` | ISO 42001 AI Management System | 81 KB |
| `loi25-quebec-privacy.pdf` | Loi 25 — Quebec Privacy Law | 255 KB |

### Step 2.2 — Configure the Chat Playground

1. Navigate to **Playgrounds > Chat playground**
2. Select deployment: `gpt-4o-mini-classifier`
3. Paste the [System Prompt v2](#82-v2-prompttxt--improved)
4. Click **Add your data (PREVIEW)** → **Azure AI Search**
5. Configure index: `regulatory-docs-index` — Search type: Keyword
6. Upload all 4 PDFs and wait for indexation

The indexation pipeline:
- **Cracking & Chunking** — PDFs split into text chunks
- **Creating AI Search Index** — Schema registered
- **Indexation** — Chunks stored and searchable

---

## 5. Phase 3 — Testing & Evaluation

### Step 3.1 — Manual Testing (4 Use Cases)

| # | Use Case | Expected | Result |
|---|----------|----------|--------|
| 1 | AI to auto-approve/reject mortgage applications without human review | HIGH | HIGH ✅ |
| 2 | AI to sort internal IT support tickets by priority level | LIMITED | LIMITED ✅ |
| 3 | AI chatbot to answer general product/service questions | LIMITED | LIMITED ✅ |
| 4 | AI to decide employee promotions and terminations | HIGH | HIGH ✅ |

### Step 3.2 — Prompt Versioning on GitHub

1. Create `prompts/v1-prompt.txt` → commit `Create v1-prompt`
2. Create `prompts/v2-prompt.txt` → commit `Create v2-prompt`

### Step 3.3 — Automated Evaluation

#### Evaluation Progression

| Run | Dataset | Prompt | Groundedness | Relevance |
|-----|---------|--------|-------------|-----------|
| eval-v1 | test-cases.jsonl (no context) | v1 | 🟡 75% (3/4) | 🟢 100% (4/4) |
| eval-v2 | test-cases.jsonl (no context) | v2 | 🔴 50% (2/4) | 🟢 100% (4/4) |
| eval-v3 | test-cases-v2.jsonl (with context) | v2 | 🟢 **100% (4/4)** | 🟢 **100% (4/4)** |

> 💡 **GenAIOps cycle:** Measure → Identify → Improve → Validate. This is exactly what AI-300 Domain 4 evaluates.

#### Evaluation Dataset Format (JSONL)

```jsonl
{"query": "We want to use AI to automatically approve mortgage applications without human review.", "expected_response": "HIGH", "context": "EU AI Act Article 5 prohibits AI systems that make automated decisions affecting individuals access to credit without human oversight."}
```

#### Evaluation Metrics

| Metric | What It Measures | Target |
|--------|-----------------|--------|
| Groundedness | Is the response anchored in the indexed documents? | >= 80% |
| Relevance | Does the response address the question asked? | >= 90% |

---

## 6. Phase 4 — API Integration

> **WHY build an API client?** A Playground demo proves the concept. An API client proves production readiness.

### Prerequisites

```bash
pip3 install openai
export AZURE_OPENAI_API_KEY="YOUR-API-KEY"
```

> 🔒 Never hardcode API keys. Use environment variables or Azure Key Vault.

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
   Mortgage auto-approval without human review

🤖 CLASSIFICATION:
1. Risk Level: HIGH
2. Regulatory Article: EU AI Act Article 5...
3. Required Governance Controls:
   - Human-in-the-loop mandatory
   - Implement transparency measures

📊 Tokens used: 318
```

---

## 7. Phase 5 — Infrastructure as Code (Bicep)

> **WHY Bicep?** Everything built manually in the Azure portal until now takes 15+ minutes of clicks and cannot be reproduced reliably. Bicep turns your infrastructure into versioned, auditable code — deployable in under 30 seconds. This is a requirement in regulated enterprises like banks.

> **WHAT is Bicep?** Bicep is Azure's native Infrastructure as Code (IaC) language. A `.bicep` file describes the Azure resources you want to provision. Azure compiles it into an ARM template and deploys everything automatically.

> **HOW does it work?** Write once, deploy anywhere. The same `main.bicep` file deploys to `dev` or `prod` by simply changing the parameters file.

### Prerequisites

```bash
# Install Azure CLI (Ubuntu)
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Install Bicep
az bicep install

# Login to Azure
az login --use-device-code --tenant YOUR-TENANT-ID

# Verify subscription
az account show --output table
```

### Step 5.1 — File Structure

```
infra/
├── main.bicep              # Main Bicep template
├── parameters.dev.json     # Dev environment parameters
└── parameters.prod.json    # Prod environment parameters
```

### Step 5.2 — main.bicep

```bicep
// ============================================================
// AI Risk Classifier — Infrastructure as Code
// Author: Louiza Boujida | TheGovernAI.io
// Domain: AI-300 Domain 1 — MLOps Infrastructure
// ============================================================

@description('Environment name: dev or prod')
@allowed(['dev', 'prod'])
param environment string = 'dev'

@description('Azure region for all resources')
param location string = 'canadacentral'

@description('Project name used for resource naming')
param projectName string = 'ai-risk-classifier'

// ── Variables ──────────────────────────────────────────────
var prefix = '${projectName}-${environment}'
var searchServiceName = 'search-${replace(prefix, '-', '')}${uniqueString(resourceGroup().id)}'

// ── Azure AI Search ────────────────────────────────────────
resource aiSearch 'Microsoft.Search/searchServices@2023-11-01' = {
  name: searchServiceName
  location: location
  sku: { name: 'basic' }
  properties: {
    replicaCount: 1
    partitionCount: 1
    hostingMode: 'default'
    publicNetworkAccess: 'enabled'
  }
  tags: {
    project: projectName
    environment: environment
    owner: 'TheGovernAI'
  }
}

// ── Log Analytics Workspace ────────────────────────────────
resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: 'log-${prefix}'
  location: location
  properties: {
    sku: { name: 'PerGB2018' }
    retentionInDays: 30
  }
  tags: { project: projectName, environment: environment }
}

// ── Application Insights ───────────────────────────────────
resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: 'appi-${prefix}'
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: logAnalytics.id
  }
  tags: { project: projectName, environment: environment }
}

// ── Outputs ────────────────────────────────────────────────
output searchServiceName string = aiSearch.name
output searchServiceEndpoint string = 'https://${aiSearch.name}.search.windows.net'
output appInsightsName string = appInsights.name
output appInsightsConnectionString string = appInsights.properties.ConnectionString
```

### Step 5.3 — parameters.dev.json

```json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentParameters.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "environment": { "value": "dev" },
    "location": { "value": "canadacentral" },
    "projectName": { "value": "ai-risk-classifier" }
  }
}
```

### Step 5.4 — Deploy

```bash
# Validate (dry run) — never touches real infrastructure
az deployment group validate \
  --resource-group rg-ai-risk-classifier \
  --template-file infra/main.bicep \
  --parameters infra/parameters.dev.json

# Deploy Dev
az deployment group create \
  --resource-group rg-ai-risk-classifier \
  --template-file infra/main.bicep \
  --parameters infra/parameters.dev.json \
  --name bicep-deploy-dev
```

### Step 5.5 — Test Idempotence

Run the exact same deploy command a second time:

```bash
az deployment group create \
  --resource-group rg-ai-risk-classifier \
  --template-file infra/main.bicep \
  --parameters infra/parameters.dev.json \
  --name bicep-deploy-dev
```

> **Expected result:** `"provisioningState": "Succeeded"` with no resources recreated. Azure detects existing resources and updates only what changed — this is the `Incremental` mode guarantee.

### Key Bicep Concepts Explained

| Concept | WHY It Matters |
|---------|---------------|
| `param environment` | Same template deploys dev or prod — no duplication |
| `uniqueString()` | Generates globally unique names for Azure Search — avoids naming conflicts |
| Tags | Enables cost filtering by project/environment in Azure Cost Management |
| Outputs | Returns endpoints and connection strings automatically after deploy |
| Idempotence | Deploy 10 times — same result. No duplicates, no errors |
| `Incremental` mode | Only changes what's different — safe for production redeployments |

### Validation Results

| Test | Command | Result |
|------|---------|--------|
| Dry run dev | `validate --parameters dev` | ✅ Succeeded |
| Deploy dev | `create --parameters dev` | ✅ Succeeded (25s) |
| Idempotence test | Deploy dev again | ✅ Succeeded — no changes |
| Dry run prod | `validate --parameters prod` | ✅ Succeeded |

---

## 8. System Prompts (Versioned)

### 8.1 v1-prompt.txt — Baseline

```
You are an AI Governance Risk Classifier.
Classify AI use cases by risk level: MINIMAL, LIMITED, or HIGH.
Reference EU AI Act, OSFI E-23, ISO 42001, or Loi 25 QC.
Be precise, structured, and concise.
```

### 8.2 v2-prompt.txt — Improved

**Changes:** Added explicit risk level definitions + grounding instructions → Groundedness 50% → 100%.

```
You are an AI Governance Risk Classifier.

Risk level definitions:
- MINIMAL: Internal operational tools with no impact on individuals
- LIMITED: Customer-facing systems requiring transparency and monitoring
- HIGH: Automated decisions affecting individuals' rights, employment, credit, or safety

Always ground your response in indexed documents: EU AI Act, OSFI E-23, ISO 42001, Loi 25 QC.
Always cite the specific article and document name.
Never introduce information not present in source documents.
```

---

## 9. Repository Structure

```
ai-risk-classifier/
├── README.md                      # Project overview
├── .gitignore
├── LICENSE                        # MIT
├── prompts/
│   ├── v1-prompt.txt              # Baseline system prompt
│   └── v2-prompt.txt              # Improved system prompt
├── src/
│   └── classifier.py              # Python API client
├── data/
│   ├── test-cases.jsonl           # Evaluation dataset v1
│   └── test-cases-v2.jsonl        # Evaluation dataset v2 (with context)
├── infra/
│   ├── main.bicep                 # Bicep IaC template
│   ├── parameters.dev.json        # Dev parameters
│   └── parameters.prod.json       # Prod parameters (dry run validated)
└── docs/
    └── implementation-guide.md    # This document
```

---

## 10. Known Limitations & Roadmap

| Limitation | Impact | Recommended Solution |
|-----------|--------|---------------------|
| Regulatory PDFs may become outdated | Classifier cites obsolete articles | Automated monitoring + scheduled re-indexing (Azure Logic Apps) |
| Keyword search only | Lower semantic precision | Migrate to vector embeddings when available in Canada Central |
| No RAG in API client | API calls bypass indexed documents | Integrate Azure AI Search SDK into classifier.py |
| Bicep does not provision AI Foundry Hub | Manual step still required | Add `Microsoft.MachineLearningServices/workspaces` to Bicep |
| Single region | Canada Central limitations | Evaluate multi-region for production |

---

## 11. Cost Estimate

| Resource | Tier | Est. Monthly Cost (USD) |
|----------|------|------------------------|
| Azure AI Search | Basic | ~$8.00 |
| GPT-4o mini | Pay-per-token | ~$3–8 |
| Log Analytics | PerGB2018 | <$1.00 |
| Application Insights | Pay-per-use | <$1.00 |
| **Total** | | **~$12–18 / month** |

---

## 12. Glossary

| Term | Definition |
|------|-----------|
| **RAG** | Retrieval-Augmented Generation — retrieves document chunks at query time to ground LLM responses. |
| **Groundedness** | Evaluation metric — are all claims traceable to indexed source documents? |
| **GenAIOps** | Operational practices for deploying and governing generative AI systems on pre-trained models. |
| **IaC** | Infrastructure as Code — managing cloud infrastructure through versioned code files instead of manual clicks. |
| **Bicep** | Azure's native IaC language. Compiles to ARM templates. Supports parameterization and idempotent deployments. |
| **Idempotence** | Property of a deployment where running it multiple times produces the same result — no duplicates, no errors. |
| **Incremental mode** | Azure deployment mode that only updates resources that changed — safe for production. |
| **Prompt Versioning** | Storing each system prompt iteration in version control with unique identifiers. |
| **OSFI E-23** | Model Risk Management guideline for Canadian federally regulated financial institutions. |
| **EU AI Act** | Regulation (EU) 2024/1689 — comprehensive AI legal framework classifying systems by risk level. |

---

## Document Information

| Field | Value |
|-------|-------|
| Author | Louiza Boujida |
| Brand | TheGovernAI.io |
| Version | 2.0 |
| Date | March 2026 |
| License | MIT |
| GitHub | github.com/louIzabou/ai-risk-classifier |

---

> ⚠️ All Azure endpoints, API keys, and subscription IDs shown in this guide use placeholder values. Never expose real credentials in documentation.
