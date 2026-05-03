from fastapi import FastAPI
from pydantic import BaseModel
from app.agents.orchestrator import OrchestratorAgent
from app.rag.vectordb import VectorDB

app = FastAPI()
vectordb = VectorDB(dim=384)
orchestrator = OrchestratorAgent(vectordb)

class JDRequest(BaseModel):
    role: str
    company_context: str

@app.post("/generate-and-evaluate")
def generate_and_evaluate(req: JDRequest):
    return orchestrator.execute(req.role, req.company_context)