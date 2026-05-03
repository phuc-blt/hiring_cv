import json
from typing import Dict, List, Any
from app.agents.base import BaseAgent

class ReportAgent(BaseAgent):
    def __init__(self):
        super().__init__("app/prompts/report_prompt.txt")
    
    def generate_comprehensive_report(self, evaluation_data: Dict) -> Dict[str, Any]:
        """
        Generate comprehensive evaluation report
        
        Args:
            evaluation_data: All evaluation data from other agents
            
        Returns:
            Dict with comprehensive report
        """
        payload = json.dumps({
            "evaluation_data": evaluation_data,
            "task": "comprehensive_report"
        }, ensure_ascii=False)
        
        return self.run(payload)
    
    def generate_executive_summary(self, full_report: Dict) -> Dict[str, Any]:
        """
        Generate executive summary for hiring managers
        
        Args:
            full_report: Complete evaluation report
            
        Returns:
            Dict with executive summary
        """
        payload = json.dumps({
            "full_report": full_report,
            "task": "executive_summary"
        }, ensure_ascii=False)
        
        return self.run(payload)
    
    def generate_candidate_feedback(self, evaluation_results: Dict) -> Dict[str, Any]:
        """
        Generate constructive feedback for candidate
        
        Args:
            evaluation_results: Evaluation results and scores
            
        Returns:
            Dict with candidate feedback
        """
        payload = json.dumps({
            "evaluation_results": evaluation_results,
            "task": "candidate_feedback"
        }, ensure_ascii=False)
        
        return self.run(payload)
    
    def generate_comparison_report(self, candidates_data: List[Dict]) -> Dict[str, Any]:
        """
        Generate comparison report for multiple candidates
        
        Args:
            candidates_data: List of candidate evaluation data
            
        Returns:
            Dict with comparison analysis
        """
        payload = json.dumps({
            "candidates_data": candidates_data,
            "task": "comparison_report"
        }, ensure_ascii=False)
        
        return self.run(payload)
    
    def generate_interview_questions(self, candidate_profile: Dict, jd_requirements: str) -> Dict[str, Any]:
        """
        Generate tailored interview questions based on candidate profile
        
        Args:
            candidate_profile: Candidate's skills and experience
            jd_requirements: Job description requirements
            
        Returns:
            Dict with interview questions
        """
        payload = json.dumps({
            "candidate_profile": candidate_profile,
            "jd_requirements": jd_requirements,
            "task": "interview_questions"
        }, ensure_ascii=False)
        
        return self.run(payload)
    
    def format_report_for_hiring_manager(self, report_data: Dict) -> Dict[str, Any]:
        """
        Format report specifically for hiring manager consumption
        
        Args:
            report_data: Raw report data
            
        Returns:
            Dict with formatted report
        """
        payload = json.dumps({
            "report_data": report_data,
            "task": "format_for_hiring_manager"
        }, ensure_ascii=False)
        
        return self.run(payload)