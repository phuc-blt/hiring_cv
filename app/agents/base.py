from app.llm.llm import LLMRouter

class BaseAgent:
    def __init__(self, prompt_path: str):
        self.router = LLMRouter()
        with open(prompt_path, "r", encoding="utf-8") as f:
            self.system_prompt = f.read()

    def run(self, payload: str):
        full_prompt = f"{self.system_prompt}\n\nINPUT:\n{payload}"
        return self.router.generate(full_prompt)