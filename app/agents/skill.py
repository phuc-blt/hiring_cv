import json
from typing import Dict, List, Any
from app.agents.base import BaseAgent

class SkillAgent(BaseAgent):
    def __init__(self):
        super().__init__("app/prompts/skill_prompt.txt")
    
    def extract_skills(self, cv_content: str, jd_requirements: str = None) -> Dict[str, Any]:
        """
        Extract and analyze skills from CV content
        
        Args:
            cv_content: The CV text content
            jd_requirements: Optional JD requirements for comparison
            
        Returns:
            Dict with extracted skills and analysis
        """
        payload = json.dumps({
            "cv_content": cv_content,
            "jd_requirements": jd_requirements
        }, ensure_ascii=False)
        
        return self.run(payload)
    
    def analyze_skill_gaps(self, candidate_skills: Dict, required_skills: Dict) -> Dict[str, Any]:
        """
        Analyze skill gaps between candidate and requirements
        
        Args:
            candidate_skills: Extracted candidate skills
            required_skills: Required skills from JD
            
        Returns:
            Dict with skill gap analysis
        """
        payload = json.dumps({
            "candidate_skills": candidate_skills,
            "required_skills": required_skills
        }, ensure_ascii=False)
        
        return self.run(payload)
    
    def categorize_skills(self, skills_text: str) -> Dict[str, List[str]]:
        """
        Categorize skills into technical, soft, and domain skills
        
        Args:
            skills_text: Raw skills text from CV
            
        Returns:
            Dict with categorized skills
        """
        payload = json.dumps({
            "skills_text": skills_text,
            "task": "categorize"
        }, ensure_ascii=False)
        
        return self.run(payload)
    
    def validate_skill_level(self, skill: str, experience_text: str) -> Dict[str, Any]:
        """
        Validate and estimate skill level based on experience
        
        Args:
            skill: Specific skill to validate
            experience_text: Experience description text
            
        Returns:
            Dict with skill level assessment
        """
        payload = json.dumps({
            "skill": skill,
            "experience_text": experience_text,
            "task": "validate_level"
        }, ensure_ascii=False)
        
        return self.run(payload)