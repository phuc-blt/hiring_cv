from app.agents.base import BaseAgent

class JDAgent(BaseAgent):
    def __init__(self):
        super().__init__("app/prompts/jd_prompt.txt")

    def generate_jd(self, role: str, company_context: str):
        payload = f"ROLE: {role}\nCOMPANY: {company_context}"
        return self.run(payload)