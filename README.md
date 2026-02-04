# OncoDetect X

## Overview
OncoDetect X is an AI-assisted cancer triage and decision-support system. It combines deep learning (simulated), deterministic risk logic, and LLM-based cognitive reasoning to provide a defensible, multi-layered risk assessment for oncology cases.

## Features
- **Multi-Organ Support**: Brain, Lung, Breast.
- **Perception Layer**: Simulates CNN analysis for initial confidence.
- **Risk Aggregation**: Combines ML scores, symptoms, and risk factors deterministically.
- **Cognitive Layer**: Uses LLM (OpenAI) to contextualize findings and generate explanations properly handling uncertainty.
- **Hospital Recommendation**: Suggests nearby facilities based on specialization.
- **Premium UI**: Modern, glassmorphism-based interface.

## Tech Stack
- **Backend**: Python FastAPI
- **Frontend**: Next.js (React), Tailwind-free (Vanilla CSS/Modules)
- **AI/LLM**: OpenAI GPT-4o integration

## Getting Started

### Prerequisites
- Node.js 18+
- Python 3.9+
- OpenAI API Key (Set in `.env` as `OPENAI_API_KEY`)

### Installation

1. **Backend**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r backend/requirements.txt
   ```

2. **Frontend**
   ```bash
   cd frontend
   npm install
   ```

### Running
- Backend: `./start_backend.sh`
- Frontend: `./start_frontend.sh`

## Disclaimer
This system is for **research and educational purposes only**. It does NOT diagnose cancer. All outputs should be verified by a medical professional.




## 🏗️ System Architecture

```mermaid
graph TD
    A[User / Clinician] -->|Uploads Scan + Patient History| B(Image Preprocessing Layer)
    B -->|Normalized Tensor| C{Organ Selector}
    
    C -->|MRI| D[Brain CNN Model]
    C -->|X-Ray| E[Lung CNN Model]
    C -->|Mammogram| F[Breast CNN Model]
    
    D & E & F -->|Feature Vector & Probability| G[Feature Extraction]
    
    G --> H[LLM Clinical Reasoning Engine]
    A -->|Text Context| H
    
    H --> I{Safety & Audit Check}
    I -->|Low Confidence| J[Flag for Human Review]
    I -->|High Confidence| K[Generate Structured Triage Report]

