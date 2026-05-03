import json
from app.agents.base import BaseAgent

class ScoringAgent(BaseAgent):
    def __init__(self):
        super().__init__("app/prompts/scoring_prompt.txt")

    def score_candidate(self, jd: str, retrieval_result: dict):
        cv_chunks = retrieval_result.get("relevant_sections", [])
        keywords = retrieval_result.get("keywords", "")
        
        payload = json.dumps({
            "jd": jd,
            "cv": cv_chunks,
            "keywords": keywords
        }, ensure_ascii=False)
        return self.run(payload)