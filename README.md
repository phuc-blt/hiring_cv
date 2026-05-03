# Multi-Agent Hiring System (JD Generation → CV RAG Retrieval → Candidate Scoring)

## Mục tiêu

Xây dựng hệ thống multi-agentic để:

1. User nhập **vị trí tuyển dụng + context công ty**
2. Hệ thống tự động tạo **JD chuẩn hóa**
3. CV gửi về được ingest + parse + chunk + embedding
4. Agent RAG retrieve CV phù hợp theo JD
5. Multi-agent scoring từng tiêu chí (skills, tools, projects, seniority, domain-fit...)
6. Trả về **score tổng + score từng mục + gap analysis + interview questions**
7. LLM routing: **Gemini ưu tiên**, nếu quota/token fail → fallback **vLLM local/OpenAI-compatible**

---

# Kiến trúc Multi-Agent

```txt
User Input (Role + Company Context)
        │
        ▼
[OrchestratorAgent]
        │
 ┌──────┼────────┬───────────────┬──────────────┐
 ▼      ▼        ▼               ▼              ▼
RoleAgent CompanyAgent JDWriterAgent SkillTaxonomyAgent ComplianceAgent
        │
        ▼
 Structured JD JSON
        │
        ▼
 CV Intake Pipeline
(Parse PDF/DOCX → OCR optional → Normalize → Chunk → Embed → Vector DB)
        │
        ▼
 RetrievalAgent (Agentic RAG)
        │
        ▼
 Evaluation Squad:
   - SkillMatchAgent
   - ProjectAgent
   - ExperienceAgent
   - ToolingAgent
   - CultureFitAgent
        │
        ▼
 ScoreAggregatorAgent
        │
        ▼
 Final Hiring Report + Ranking
```

---

# Scoring Framework (Ví dụ AI Engineer)

```json
{
  "weights": {
    "core_ai_ml": 0.25,
    "llm_rag": 0.20,
    "projects": 0.20,
    "tools_stack": 0.15,
    "experience_years": 0.10,
    "domain_fit": 0.05,
    "communication": 0.05
  }
}
```

### Các tiêu chí:

* Python, ML/DL, Transformers
* LLM, RAG, vector DB, prompt engineering
* Production deployment (FastAPI, Docker, K8s)
* Cloud / MLOps
* Real project outcomes
* Leadership / ownership

---

# Project Structure

```txt
multi_agent_hiring/
│
├── app/
│   ├── main.py
│   ├── config.py
│   ├── llm/
│   │   └── llm_router.py
│   ├── agents/
│   │   ├── base_agent.py
│   │   ├── orchestrator_agent.py
│   │   ├── jd_agent.py
│   │   ├── retrieval_agent.py
│   │   ├── skill_match_agent.py
│   │   ├── project_agent.py
│   │   ├── scoring_agent.py
│   │   └── report_agent.py
│   ├── rag/
│   │   ├── parser.py
│   │   ├── embedder.py
│   │   └── vectordb.py
│   ├── prompts/
│   │   ├── jd_prompt.txt
│   │   ├── retrieval_prompt.txt
│   │   ├── scoring_prompt.txt
│   │   └── report_prompt.txt
│   └── schemas/
│       └── models.py
│
├── README.md
├── requirements.txt
└── .env
```

---

# requirements.txt

```txt
fastapi
uvicorn
pydantic
google-generativeai
openai
sentence-transformers
faiss-cpu
pypdf
python-docx
tenacity
```

---

# .env

```env
GEMINI_API_KEY=your_key
VLLM_BASE_URL=http://localhost:8000/v1
VLLM_API_KEY=dummy
PRIMARY_MODEL=gemini-2.5-pro
FALLBACK_MODEL=meta-llama/Meta-Llama-3-8B-Instruct
```

---

---

# Prompt Example: app/prompts/scoring_prompt.txt

```txt
You are a senior technical recruiter AI.
Evaluate candidate against JD.
Return JSON:
{
  "overall_score": 0-100,
  "skills_score": 0-100,
  "project_score": 0-100,
  "tools_score": 0-100,
  "experience_score": 0-100,
  "strengths": [],
  "gaps": [],
  "interview_questions": []
}
Be strict, evidence-based, and reference CV sections.
```

---

# README.md

## Run vLLM

```bash
python -m vllm.entrypoints.openai.api_server \
  --model meta-llama/Meta-Llama-3-8B-Instruct \
  --port 8000
```

## Run API

```bash
uvicorn app.main:app --reload
```

## API Call

```bash
curl -X POST http://127.0.0.1:8000/generate-and-evaluate \
-H "Content-Type: application/json" \
-d '{
  "role": "AI Engineer",
  "company_context": "Building enterprise RAG systems"
}'
```

---

# Advanced Roadmap (OSCH = Orchestration Strategy Chain Hub)

## Phase 1

* JD generation
* CV parsing
* Basic RAG retrieval
* Scorecard JSON

## Phase 2

* Agent memory
* Company benchmark DB
* Candidate ranking leaderboard
* Multi-CV batch compare

## Phase 3

* Interview simulation agent
* Offer-fit prediction
* Salary benchmark agent
* Bias audit + fairness checker

---

# Best Practices

* JSON schema validation on all outputs
* Guardrails for hallucination
* Weighted scoring configurable per role
* Separate taxonomy by domain:

  * AI Engineer
  * Backend
  * PM
  * Data Scientist
* Add recruiter override panel

---

# Ý tưởng nâng cao

* Graph-based agent workflow (LangGraph / CrewAI style)
* Hybrid retrieval: semantic + keyword + section-aware
* Skill ontology normalization (PyTorch = DL framework)
* Red flag detector:

  * keyword stuffing
  * fake project inflation
  * inconsistent timeline

---

## Kết quả

Hệ thống này hoạt động như một **AI Recruiter OS**, không chỉ generate JD mà còn transform hiring thành pipeline tự động, có thể scale cho enterprise hiring.
CUDA_VISIBLE_DEVICES=2,3 \
HF_HOME=/workspace/phucnt/models/ \
python -m vllm.entrypoints.openai.api_server \
  --model Qwen/Qwen3.5-9B \
  --tensor-parallel-size 2 \
  --dtype bfloat16 \
  --gpu-memory-utilization 0.7 \
  --max-model-len 8192 \
  --enforce-eager \
  --host 0.0.0.0 \
  --port 3000# hiring_cv
