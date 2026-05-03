import json
from typing import Dict, List, Any
from app.agents.base import BaseAgent

class ProjectAgent(BaseAgent):
    def __init__(self):
        super().__init__("app/prompts/project_prompt.txt")
    
    def extract_projects(self, cv_content: str) -> Dict[str, Any]:
        """
        Extract project information from CV content
        
        Args:
            cv_content: The CV text content
            
        Returns:
            Dict with extracted projects and analysis
        """
        payload = json.dumps({
            "cv_content": cv_content,
            "task": "extract_projects"
        }, ensure_ascii=False)
        
        return self.run(payload)
    
    def analyze_project_relevance(self, projects: List[Dict], jd_requirements: str) -> Dict[str, Any]:
        """
        Analyze relevance of projects to job requirements
        
        Args:
            projects: List of extracted projects
            jd_requirements: Job description requirements
            
        Returns:
            Dict with relevance analysis
        """
        payload = json.dumps({
            "projects": projects,
            "jd_requirements": jd_requirements,
            "task": "analyze_relevance"
        }, ensure_ascii=False)
        
        return self.run(payload)
    
    def assess_project_complexity(self, project_description: str) -> Dict[str, Any]:
        """
        Assess the complexity and scale of a project
        
        Args:
            project_description: Description of the project
            
        Returns:
            Dict with complexity assessment
        """
        payload = json.dumps({
            "project_description": project_description,
            "task": "assess_complexity"
        }, ensure_ascii=False)
        
        return self.run(payload)
    
    def extract_technical_stack(self, project_text: str) -> Dict[str, List[str]]:
        """
        Extract technical stack used in projects
        
        Args:
            project_text: Text describing projects
            
        Returns:
            Dict with categorized technical stack
        """
        payload = json.dumps({
            "project_text": project_text,
            "task": "extract_tech_stack"
        }, ensure_ascii=False)
        
        return self.run(payload)
    
    def evaluate_project_impact(self, project_details: Dict) -> Dict[str, Any]:
        """
        Evaluate the impact and achievements of projects
        
        Args:
            project_details: Detailed project information
            
        Returns:
            Dict with impact evaluation
        """
        payload = json.dumps({
            "project_details": project_details,
            "task": "evaluate_impact"
        }, ensure_ascii=False)
        
        return self.run(payload)