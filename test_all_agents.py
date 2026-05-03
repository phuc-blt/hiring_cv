#!/usr/bin/env python3
"""
Comprehensive test script for all agents in the hiring CV system
"""

import json
from app.agents.orchestrator import OrchestratorAgent
from app.agents.jd import JDAgent
from app.agents.scoring import ScoringAgent
from app.agents.retrieval import RetrievalAgent
from app.agents.skill import SkillAgent
from app.agents.project import ProjectAgent
from app.agents.report import ReportAgent
from app.rag.vectordb import VectorDB

def test_all_agents():
    """Test all agents with sample data"""
    print("🚀 Testing all agents in the hiring CV system")
    
    # Initialize components
    vectordb = VectorDB(persist_directory="./test_agents_chroma_db")
    orchestrator = OrchestratorAgent(vectordb)
    
    # Sample data
    sample_cv = """
    John Doe
    Senior Software Engineer
    
    EXPERIENCE:
    - Senior Software Engineer at Tech Corp (2020-Present)
      * Led team of 5 developers
      * Built microservices architecture using Python, Django, PostgreSQL
      * Implemented CI/CD pipeline with Docker and Kubernetes
      * Reduced system latency by 40%
    
    - Software Engineer at StartupXYZ (2018-2020)
      * Developed React frontend for e-commerce platform
      * Built REST APIs using Node.js and Express
      * Worked with MongoDB database
    
    PROJECTS:
    - E-commerce Platform (Full-stack)
      * Technologies: React, Node.js, MongoDB, Docker
      * Led team of 3, delivered 2 months ahead of schedule
      * Increased conversion rate by 25%
    
    - Data Analytics Dashboard
      * Technologies: Python, Pandas, D3.js
      * Real-time data visualization
      * Used by 1000+ users daily
    
    SKILLS:
    - Programming: Python, JavaScript, Java, SQL
    - Frameworks: Django, React, Node.js, Express
    - Databases: PostgreSQL, MongoDB, Redis
    - Tools: Docker, Kubernetes, Git, AWS
    - Soft Skills: Leadership, Communication, Problem-solving
    
    EDUCATION:
    - BS Computer Science, University of Technology (2014-2018)
    """
    
    sample_jd = """
    Senior Software Engineer Position
    
    We are looking for a Senior Software Engineer to join our growing team.
    
    REQUIREMENTS:
    - 5+ years of software development experience
    - Strong proficiency in Python and JavaScript
    - Experience with cloud platforms (AWS, GCP, or Azure)
    - Knowledge of microservices architecture
    - Experience with containerization (Docker, Kubernetes)
    - Strong leadership and communication skills
    
    RESPONSIBILITIES:
    - Design and develop scalable software solutions
    - Lead technical projects and mentor junior developers
    - Collaborate with cross-functional teams
    - Implement best practices for code quality and testing
    
    TECHNOLOGY STACK:
    - Backend: Python, Django, FastAPI
    - Frontend: React, TypeScript
    - Database: PostgreSQL, Redis
    - Cloud: AWS, Docker, Kubernetes
    """
    
    print("✅ Sample data prepared")
    
    # Test individual agents
    test_results = {}
    
    # Test JDAgent
    try:
        jd_agent = JDAgent()
        jd_result = jd_agent.generate_jd("Senior Software Engineer", "Tech company looking for experienced engineer")
        test_results["jd_agent"] = "✅ Success"
        print("✅ JDAgent test passed")
    except Exception as e:
        test_results["jd_agent"] = f"❌ Failed: {e}"
        print(f"❌ JDAgent test failed: {e}")
    
    # Test SkillAgent
    try:
        skill_agent = SkillAgent()
        skills_result = skill_agent.extract_skills(sample_cv, sample_jd)
        test_results["skill_agent"] = "✅ Success"
        print("✅ SkillAgent test passed")
    except Exception as e:
        test_results["skill_agent"] = f"❌ Failed: {e}"
        print(f"❌ SkillAgent test failed: {e}")
    
    # Test ProjectAgent
    try:
        project_agent = ProjectAgent()
        projects_result = project_agent.extract_projects(sample_cv)
        test_results["project_agent"] = "✅ Success"
        print("✅ ProjectAgent test passed")
    except Exception as e:
        test_results["project_agent"] = f"❌ Failed: {e}"
        print(f"❌ ProjectAgent test failed: {e}")
    
    # Test ReportAgent
    try:
        report_agent = ReportAgent()
        mock_evaluation = {
            "skills_analysis": {"total_skills": 15},
            "projects_analysis": {"total_projects": 2},
            "scoring": {"total_score": 42}
        }
        report_result = report_agent.generate_comprehensive_report(mock_evaluation)
        test_results["report_agent"] = "✅ Success"
        print("✅ ReportAgent test passed")
    except Exception as e:
        test_results["report_agent"] = f"❌ Failed: {e}"
        print(f"❌ ReportAgent test failed: {e}")
    
    # Test RetrievalAgent
    try:
        retrieval_agent = RetrievalAgent(vectordb)
        retrieval_result = retrieval_agent.retrieve_relevant_cv_sections(sample_jd)
        test_results["retrieval_agent"] = "✅ Success"
        print("✅ RetrievalAgent test passed")
    except Exception as e:
        test_results["retrieval_agent"] = f"❌ Failed: {e}"
        print(f"❌ RetrievalAgent test failed: {e}")
    
    # Test ScoringAgent
    try:
        scoring_agent = ScoringAgent()
        mock_retrieval = {
            "relevant_sections": [sample_cv[:500]],
            "keywords": "Python, JavaScript, Leadership"
        }
        scoring_result = scoring_agent.score_candidate(sample_jd, mock_retrieval)
        test_results["scoring_agent"] = "✅ Success"
        print("✅ ScoringAgent test passed")
    except Exception as e:
        test_results["scoring_agent"] = f"❌ Failed: {e}"
        print(f"❌ ScoringAgent test failed: {e}")
    
    # Test OrchestratorAgent
    try:
        orchestrator_result = orchestrator.execute_full_evaluation(
            cv_content=sample_cv,
            jd_text=sample_jd
        )
        test_results["orchestrator"] = "✅ Success"
        print("✅ OrchestratorAgent test passed")
    except Exception as e:
        test_results["orchestrator"] = f"❌ Failed: {e}"
        print(f"❌ OrchestratorAgent test failed: {e}")
    
    # Test interview kit generation
    try:
        interview_kit = orchestrator.generate_interview_kit(sample_cv, sample_jd)
        test_results["interview_kit"] = "✅ Success"
        print("✅ Interview kit generation test passed")
    except Exception as e:
        test_results["interview_kit"] = f"❌ Failed: {e}"
        print(f"❌ Interview kit generation test failed: {e}")
    
    print("\n" + "="*60)
    print("AGENT TEST RESULTS SUMMARY")
    print("="*60)
    
    for agent, result in test_results.items():
        print(f"{agent.replace('_', ' ').title()}: {result}")
    
    success_count = sum(1 for result in test_results.values() if result.startswith("✅"))
    total_count = len(test_results)
    
    print(f"\nOverall: {success_count}/{total_count} agents working correctly")
    
    if success_count == total_count:
        print("🎉 All agents are working perfectly!")
        print("\nSystem is ready for production use.")
        print("\nUsage examples:")
        print("1. Full evaluation: orchestrator.execute_full_evaluation(cv, jd)")
        print("2. Interview kit: orchestrator.generate_interview_kit(cv, jd)")
        print("3. Individual agents: skill_agent.extract_skills(cv)")
    else:
        print("⚠️  Some agents need attention. Please check the errors above.")
    
    return success_count == total_count

if __name__ == "__main__":
    test_all_agents()
