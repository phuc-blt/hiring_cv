from app.agents.base import BaseAgent

class RetrievalAgent(BaseAgent):
    def __init__(self, vectordb):
        super().__init__("app/prompts/retrieval_prompt.txt")
        self.vectordb = vectordb

    def retrieve_relevant_cv_sections(self, jd_text: str):
        # Use prompt to extract keywords first
        keywords_result = self.run(jd_text)
        
        # Search using the JD text directly with new RAG system
        relevant_sections = self.vectordb.search(jd_text, k=10)
        
        return {
            "keywords": keywords_result,
            "relevant_sections": relevant_sections
        }