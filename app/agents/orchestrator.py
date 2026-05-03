from app.agents.jd import JDAgent
from app.agents.scoring import ScoringAgent
from app.agents.retrieval import RetrievalAgent
from app.agents.skill import SkillAgent
from app.agents.project import ProjectAgent
from app.agents.report import ReportAgent

class OrchestratorAgent:
    def __init__(self, vectordb):
        self.jd_agent = JDAgent()
        self.retrieval_agent = RetrievalAgent(vectordb)
        self.scoring_agent = ScoringAgent()
        self.skill_agent = SkillAgent()
        self.project_agent = ProjectAgent()
        self.report_agent = ReportAgent()

    def execute_full_evaluation(self, cv_content: str, jd_text: str = None, role: str = None, company_context: str = None):
        """
        Execute comprehensive candidate evaluation using all agents
        
        Args:
            cv_content: CV text content
            jd_text: Job description text (optional, will generate if not provided)
            role: Job role (optional)
            company_context: Company context (optional)
            
        Returns:
            Dict with comprehensive evaluation results
        """
        try:
            # Generate JD if not provided
            if not jd_text and role and company_context:
                jd_text = self.jd_agent.generate_jd(role, company_context)
            
            # Extract skills
            skills_result = self.skill_agent.extract_skills(cv_content, jd_text)
            if isinstance(skills_result, str):
                skills_result = {"raw_result": skills_result}
            
            # Extract projects
            projects_result = self.project_agent.extract_projects(cv_content)
            if isinstance(projects_result, str):
                projects_result = {"raw_result": projects_result}
            
            # Analyze project relevance if JD is available
            projects_analysis = {}
            if jd_text and projects_result and projects_result.get("extracted_projects"):
                projects_analysis = self.project_agent.analyze_project_relevance(
                    projects_result["extracted_projects"], 
                    jd_text
                )
                if isinstance(projects_analysis, str):
                    projects_analysis = {"raw_result": projects_analysis}
            else:
                projects_analysis = {}
            
            # RAG retrieval for additional context
            retrieval_result = self.retrieval_agent.retrieve_relevant_cv_sections(jd_text or cv_content)
            if isinstance(retrieval_result, str):
                retrieval_result = {"keywords": retrieval_result, "relevant_sections": []}
            elif not isinstance(retrieval_result, dict):
                retrieval_result = {"keywords": "", "relevant_sections": []}
            
            # Ensure retrieval_result has required keys for scoring
            if "relevant_sections" not in retrieval_result:
                retrieval_result["relevant_sections"] = []
            if "keywords" not in retrieval_result:
                retrieval_result["keywords"] = ""
            
            # Scoring
            scoring_result = self.scoring_agent.score_candidate(jd_text or "", retrieval_result)
            if isinstance(scoring_result, str):
                scoring_result = {"raw_result": scoring_result}
            
            # Generate comprehensive report
            evaluation_data = {
                "skills_analysis": skills_result,
                "projects_analysis": projects_analysis,
                "scoring": scoring_result,
                "retrieval": retrieval_result,
                "jd_text": jd_text
            }
            
            comprehensive_report = self.report_agent.generate_comprehensive_report(evaluation_data)
            if not isinstance(comprehensive_report, str):
                comprehensive_report = str(comprehensive_report)
            
            # Generate executive summary
            executive_summary = self.report_agent.generate_executive_summary(comprehensive_report)
            if not isinstance(executive_summary, str):
                executive_summary = str(executive_summary)
            
            return {
                "skills_analysis": skills_result,
                "projects_analysis": projects_analysis,
                "scoring": scoring_result,
                "retrieval": retrieval_result,
                "comprehensive_report": comprehensive_report,
                "executive_summary": executive_summary,
                "jd_text": jd_text
            }
            
        except Exception as e:
            print(f"Error in execute_full_evaluation: {str(e)}")
            import traceback
            traceback.print_exc()
            
            # Return fallback result
            return {
                "skills_analysis": {"error": str(e)},
                "projects_analysis": {"error": str(e)},
                "scoring": {"error": str(e)},
                "retrieval": {"error": str(e), "keywords": "", "relevant_sections": []},
                "comprehensive_report": f"Evaluation failed due to error: {str(e)}",
                "executive_summary": f"Evaluation failed: {str(e)}",
                "jd_text": jd_text
            }
    
    def execute(self, role: str, company_context: str):
        """Original method for backward compatibility"""
        jd = self.jd_agent.generate_jd(role, company_context)
        retrieval_result = self.retrieval_agent.retrieve_relevant_cv_sections(jd)
        result = self.scoring_agent.score_candidate(jd, retrieval_result)
        return {
            "jd": jd,
            "retrieval": retrieval_result,
            "evaluation": result
        }
    
    def generate_interview_kit(self, cv_content: str, jd_text: str):
        """
        Generate interview kit including questions and talking points
        
        Args:
            cv_content: CV text content
            jd_text: Job description text
            
        Returns:
            Dict with interview preparation materials
        """
        # Extract candidate profile
        skills_result = self.skill_agent.extract_skills(cv_content, jd_text)
        projects_result = self.project_agent.extract_projects(cv_content)
        
        candidate_profile = {
            "skills": skills_result,
            "projects": projects_result
        }
        
        # Generate interview questions
        interview_questions = self.report_agent.generate_interview_questions(candidate_profile, jd_text)
        
        # Generate candidate feedback points
        feedback_points = self.report_agent.generate_candidate_feedback({
            "skills": skills_result,
            "projects": projects_result
        })
        
        return {
            "candidate_profile": candidate_profile,
            "interview_questions": interview_questions,
            "feedback_points": feedback_points
        }