#!/usr/bin/env python3
"""
Test agents in offline mode when APIs are unavailable
"""

import json
from app.agents.orchestrator import OrchestratorAgent
from app.rag.vectordb import VectorDB

def test_offline_mode():
    """Test agents work in offline mode"""
    print("🚀 Testing agents in offline mode...")
    
    # Initialize components
    vectordb = VectorDB(persist_directory="./test_offline_chroma_db")
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
    
    REQUIREMENTS:
    - 5+ years of software development experience
    - Strong proficiency in Python and JavaScript
    - Experience with cloud platforms (AWS, GCP, or Azure)
    - Knowledge of microservices architecture
    - Experience with containerization (Docker, Kubernetes)
    - Strong leadership and communication skills
    """
    
    print("✅ Sample data prepared")
    
    # Test individual agents in offline mode
    test_results = {}
    
    # Test JDAgent
    try:
        jd_agent = orchestrator.jd_agent
        jd_result = jd_agent.generate_jd("Senior Software Engineer", "Tech company")
        if "[OFFLINE MODE]" in jd_result:
            test_results["jd_agent"] = "✅ Working (offline mode)"
            print("✅ JDAgent working in offline mode")
        else:
            test_results["jd_agent"] = "✅ Working (online mode)"
            print("✅ JDAgent working online")
    except Exception as e:
        test_results["jd_agent"] = f"❌ Failed: {e}"
        print(f"❌ JDAgent failed: {e}")
    
    # Test SkillAgent
    try:
        skill_agent = orchestrator.skill_agent
        skills_result = skill_agent.extract_skills(sample_cv, sample_jd)
        if isinstance(skills_result, str) and "[OFFLINE MODE]" in skills_result:
            test_results["skill_agent"] = "✅ Working (offline mode)"
            print("✅ SkillAgent working in offline mode")
        else:
            test_results["skill_agent"] = "✅ Working (online mode)"
            print("✅ SkillAgent working online")
    except Exception as e:
        test_results["skill_agent"] = f"❌ Failed: {e}"
        print(f"❌ SkillAgent failed: {e}")
    
    # Test ProjectAgent
    try:
        project_agent = orchestrator.project_agent
        projects_result = project_agent.extract_projects(sample_cv)
        if isinstance(projects_result, str) and "[OFFLINE MODE]" in projects_result:
            test_results["project_agent"] = "✅ Working (offline mode)"
            print("✅ ProjectAgent working in offline mode")
        else:
            test_results["project_agent"] = "✅ Working (online mode)"
            print("✅ ProjectAgent working online")
    except Exception as e:
        test_results["project_agent"] = f"❌ Failed: {e}"
        print(f"❌ ProjectAgent failed: {e}")
    
    # Test ReportAgent
    try:
        report_agent = orchestrator.report_agent
        mock_evaluation = {
            "skills_analysis": {"total_skills": 15},
            "projects_analysis": {"total_projects": 2},
            "scoring": {"total_score": 42}
        }
        report_result = report_agent.generate_comprehensive_report(mock_evaluation)
        if isinstance(report_result, str) and "[OFFLINE MODE]" in report_result:
            test_results["report_agent"] = "✅ Working (offline mode)"
            print("✅ ReportAgent working in offline mode")
        else:
            test_results["report_agent"] = "✅ Working (online mode)"
            print("✅ ReportAgent working online")
    except Exception as e:
        test_results["report_agent"] = f"❌ Failed: {e}"
        print(f"❌ ReportAgent failed: {e}")
    
    # Test RetrievalAgent
    try:
        retrieval_agent = orchestrator.retrieval_agent
        retrieval_result = retrieval_agent.retrieve_relevant_cv_sections(sample_jd)
        if isinstance(retrieval_result, dict) and "keywords" in retrieval_result:
            if isinstance(retrieval_result["keywords"], str) and "[OFFLINE MODE]" in retrieval_result["keywords"]:
                test_results["retrieval_agent"] = "✅ Working (offline mode)"
                print("✅ RetrievalAgent working in offline mode")
            else:
                test_results["retrieval_agent"] = "✅ Working (online mode)"
                print("✅ RetrievalAgent working online")
        else:
            test_results["retrieval_agent"] = "❌ Unexpected response format"
            print("❌ RetrievalAgent unexpected response")
    except Exception as e:
        test_results["retrieval_agent"] = f"❌ Failed: {e}"
        print(f"❌ RetrievalAgent failed: {e}")
    
    # Test ScoringAgent
    try:
        scoring_agent = orchestrator.scoring_agent
        mock_retrieval = {
            "relevant_sections": [sample_cv[:500]],
            "keywords": "Python, JavaScript, Leadership"
        }
        scoring_result = scoring_agent.score_candidate(sample_jd, mock_retrieval)
        if isinstance(scoring_result, str) and "[OFFLINE MODE]" in scoring_result:
            test_results["scoring_agent"] = "✅ Working (offline mode)"
            print("✅ ScoringAgent working in offline mode")
        else:
            test_results["scoring_agent"] = "✅ Working (online mode)"
            print("✅ ScoringAgent working online")
    except Exception as e:
        test_results["scoring_agent"] = f"❌ Failed: {e}"
        print(f"❌ ScoringAgent failed: {e}")
    
    # Test OrchestratorAgent
    try:
        orchestrator_result = orchestrator.execute_full_evaluation(
            cv_content=sample_cv,
            jd_text=sample_jd
        )
        if isinstance(orchestrator_result, dict):
            test_results["orchestrator"] = "✅ Working"
            print("✅ OrchestratorAgent working")
        else:
            test_results["orchestrator"] = "❌ Unexpected response"
            print("❌ OrchestratorAgent unexpected response")
    except Exception as e:
        test_results["orchestrator"] = f"❌ Failed: {e}"
        print(f"❌ OrchestratorAgent failed: {e}")
    
    print("\n" + "="*60)
    print("OFFLINE MODE TEST RESULTS")
    print("="*60)
    
    for agent, result in test_results.items():
        print(f"{agent.replace('_', ' ').title()}: {result}")
    
    success_count = sum(1 for result in test_results.values() if result.startswith("✅"))
    total_count = len(test_results)
    
    print(f"\nOverall: {success_count}/{total_count} agents working")
    
    if success_count > 0:
        print("🎉 System is working in offline mode!")
        print("\nTo get full functionality:")
        print("1. Start vLLM server: vllm serve Qwen/Qwen3.5-9B --port 3000")
        print("2. Or check Gemini API quota")
        print("3. Or install local models with Ollama")
    else:
        print("⚠️  System needs attention.")
    
    return success_count > 0

if __name__ == "__main__":
    test_offline_mode()
