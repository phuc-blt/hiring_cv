from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import json
import os
from datetime import datetime

from app.agents.orchestrator import OrchestratorAgent
from app.agents.jd import JDAgent
from app.agents.scoring import ScoringAgent
from app.agents.retrieval import RetrievalAgent
from app.agents.skill import SkillAgent
from app.agents.project import ProjectAgent
from app.agents.report import ReportAgent
from app.rag.vectordb import VectorDB

app = FastAPI(title="Hiring CV System API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)
vectordb = VectorDB()
orchestrator = OrchestratorAgent(vectordb)

# Data Models
class JDRequest(BaseModel):
    jobTitle: str
    department: str
    location: str
    jobType: str
    experience: str
    salary: Optional[str] = None
    description: str
    requirements: List[str]
    benefits: Optional[List[str]] = None
    platforms: List[str]

class ApplicationRequest(BaseModel):
    fullName: str
    email: str
    phone: str
    address: str
    position: str
    experience: str
    coverLetter: str
    portfolio: Optional[str] = None
    expectedSalary: Optional[str] = None
    availability: str

class CVParseRequest(BaseModel):
    cv_content: str
    jd_text: Optional[str] = None
    role: Optional[str] = None
    company_context: Optional[str] = None

class CVParseResponse(BaseModel):
    skills_analysis: Dict[str, Any]
    projects_analysis: Dict[str, Any]
    scoring: Dict[str, Any]
    retrieval: Dict[str, Any]
    comprehensive_report: str
    executive_summary: str
    jd_text: Optional[str] = None

class CandidateEvaluation(BaseModel):
    id: str
    name: str
    position: str
    email: str
    phone: str
    experience: str
    appliedDate: str
    status: str
    score: Optional[int] = None
    cvUrl: str
    coverLetter: str
    skills: List[str]
    notes: Optional[str] = None

# In-memory storage for demo (in production, use database)
applications_db = []
candidates_db = []

# JD Creation and Posting Endpoints
@app.post("/api/jd/create", response_model=Dict[str, Any])
async def create_jd(jd_request: JDRequest):
    """
    Create Job Description using AI agent and prepare for posting
    """
    try:
        # Generate enhanced JD using AI agent
        jd_agent = JDAgent()
        company_context = f"""
        Department: {jd_request.department}
        Location: {jd_request.location}
        Job Type: {jd_request.jobType}
        Experience Level: {jd_request.experience}
        Salary: {jd_request.salary}
        Benefits: {', '.join(jd_request.benefits) if jd_request.benefits else 'Not specified'}
        """
        
        enhanced_jd = jd_agent.generate_jd(jd_request.jobTitle, company_context)
        
        # Save JD to database
        jd_data = {
            "id": f"jd_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "jobTitle": jd_request.jobTitle,
            "department": jd_request.department,
            "location": jd_request.location,
            "jobType": jd_request.jobType,
            "experience": jd_request.experience,
            "salary": jd_request.salary,
            "description": jd_request.description,
            "requirements": jd_request.requirements,
            "benefits": jd_request.benefits,
            "platforms": jd_request.platforms,
            "enhanced_jd": enhanced_jd,
            "created_at": datetime.now().isoformat(),
            "status": "draft"
        }
        
        return {
            "success": True,
            "id": jd_data["id"],
            "jobTitle": jd_data["jobTitle"],
            "department": jd_data["department"],
            "location": jd_data["location"],
            "jobType": jd_data["jobType"],
            "experience": jd_data["experience"],
            "salary": jd_data["salary"],
            "description": jd_data["description"],
            "requirements": jd_data["requirements"],
            "benefits": jd_data["benefits"],
            "platforms": jd_data["platforms"],
            "enhanced_jd": enhanced_jd,
            "message": "Job description created successfully. Please review and confirm to post."
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating JD: {str(e)}")

@app.post("/api/jd/{jd_id}/post", response_model=Dict[str, Any])
async def post_jd(jd_id: str):
    """
    Post Job Description to selected platforms
    """
    try:
        # TODO: Retrieve JD from database using jd_id
        # For now, simulate posting
        posting_results = {
            "linkedin": {"status": "success", "message": "Posted to LinkedIn successfully"},
            "indeed": {"status": "success", "message": "Posted to Indeed successfully"},
            "vietnamworks": {"status": "success", "message": "Posted to VietnamWorks successfully"},
            "topcv": {"status": "success", "message": "Posted to TopCV successfully"},
            "careerbuilder": {"status": "success", "message": "Posted to CareerBuilder successfully"}
        }
        
        return {
            "success": True,
            "jd_id": jd_id,
            "posting_results": posting_results,
            "message": "Job description posted successfully to all platforms"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error posting JD: {str(e)}")

@app.get("/api/jd/list", response_model=List[Dict[str, Any]])
async def list_jds():
    """
    List all created job descriptions
    """
    # TODO: Implement database query
    return []

# Application Submission Endpoints
@app.post("/api/apply/submit", response_model=Dict[str, Any])
async def submit_application(
    fullName: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    address: str = Form(...),
    position: str = Form(...),
    experience: str = Form(...),
    coverLetter: str = Form(...),
    portfolio: Optional[str] = Form(None),
    expectedSalary: Optional[str] = Form(None),
    availability: str = Form(...),
    cvFile: UploadFile = File(...)
):
    """
    Submit job application with CV
    """
    try:
        # Save uploaded CV
        cv_filename = f"cv_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{cvFile.filename}"
        cv_path = f"uploads/{cv_filename}"
        
        # TODO: Save file to storage
        # with open(cv_path, "wb") as buffer:
        #     content = await cvFile.read()
        #     buffer.write(content)
        
        # Extract CV content
        cv_content = f"CV content for {fullName}"  # TODO: Parse actual CV content
        
        # Create application record
        application = {
            "id": f"app_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "fullName": fullName,
            "email": email,
            "phone": phone,
            "address": address,
            "position": position,
            "experience": experience,
            "coverLetter": coverLetter,
            "portfolio": portfolio,
            "expectedSalary": expectedSalary,
            "availability": availability,
            "cv_filename": cv_filename,
            "cv_path": cv_path,
            "cv_content": cv_content,
            "submitted_at": datetime.now().isoformat(),
            "status": "pending"
        }
        
        applications_db.append(application)
        
        # Add to candidates list for evaluation
        candidate = CandidateEvaluation(
            id=application["id"],
            name=fullName,
            email=email,
            phone=phone,
            position=position,
            experience=experience,
            appliedDate=application["submitted_at"][:10],
            status="pending",
            cvUrl=cv_path,
            coverLetter=coverLetter,
            skills=[],  # Will be filled after CV parsing
            notes=None
        )
        candidates_db.append(candidate)
        
        return {
            "success": True,
            "application_id": application["id"],
            "message": "Application submitted successfully",
            "status": "pending_evaluation"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error submitting application: {str(e)}")

@app.get("/api/applications/list", response_model=List[Dict[str, Any]])
async def list_applications():
    """
    List all submitted applications
    """
    return applications_db

# CV Evaluation Endpoints
@app.post("/api/evaluate/cv", response_model=CVParseResponse)
async def evaluate_cv(request: CVParseRequest):
    """
    Evaluate CV using AI agents
    """
    try:
        print(f"Starting CV evaluation for: {request.role}")
        print(f"CV content length: {len(request.cv_content)}")
        
        # Use orchestrator for comprehensive evaluation
        result = orchestrator.execute_full_evaluation(
            cv_content=request.cv_content,
            jd_text=request.jd_text,
            role=request.role,
            company_context=request.company_context
        )
        
        print(f"Evaluation result type: {type(result)}")
        print(f"Evaluation result keys: {result.keys() if isinstance(result, dict) else 'Not a dict'}")
        
        # Ensure all required fields are present and properly formatted
        formatted_result = {
            "skills_analysis": result.get("skills_analysis", {}),
            "projects_analysis": result.get("projects_analysis", {}),
            "scoring": result.get("scoring", {}),
            "retrieval": result.get("retrieval", {}),
            "comprehensive_report": result.get("comprehensive_report", ""),
            "executive_summary": result.get("executive_summary", ""),
            "jd_text": result.get("jd_text")
        }
        
        return CVParseResponse(**formatted_result)
        
    except Exception as e:
        print(f"Error in CV evaluation: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error evaluating CV: {str(e)}")

@app.post("/api/evaluate/cv-file", response_model=CVParseResponse)
async def evaluate_cv_file(
    cvFile: UploadFile = File(...),
    jd_text: Optional[str] = Form(None),
    role: Optional[str] = Form(None),
    company_context: Optional[str] = Form(None)
):
    """
    Evaluate uploaded CV file
    """
    try:
        # Read and parse CV content
        content = await cvFile.read()
        cv_content = content.decode('utf-8')  # TODO: Add proper PDF/DOC parsing
        
        # Evaluate CV
        result = orchestrator.execute_full_evaluation(
            cv_content=cv_content,
            jd_text=jd_text,
            role=role,
            company_context=company_context
        )
        
        return CVParseResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluating CV file: {str(e)}")

@app.get("/api/candidates/list", response_model=List[CandidateEvaluation])
async def list_candidates():
    """
    List all candidates for evaluation
    """
    return candidates_db

@app.put("/api/candidates/{candidate_id}/status")
async def update_candidate_status(candidate_id: str, status: str):
    """
    Update candidate evaluation status
    """
    for candidate in candidates_db:
        if candidate.id == candidate_id:
            candidate.status = status
            return {"success": True, "message": "Status updated successfully"}
    
    raise HTTPException(status_code=404, detail="Candidate not found")

@app.put("/api/candidates/{candidate_id}/score")
async def update_candidate_score(candidate_id: str, score: int):
    """
    Update candidate score
    """
    for candidate in candidates_db:
        if candidate.id == candidate_id:
            candidate.score = score
            return {"success": True, "message": "Score updated successfully"}
    
    raise HTTPException(status_code=404, detail="Candidate not found")

@app.put("/api/candidates/{candidate_id}/notes")
async def update_candidate_notes(candidate_id: str, notes: str):
    """
    Update candidate evaluation notes
    """
    for candidate in candidates_db:
        if candidate.id == candidate_id:
            candidate.notes = notes
            return {"success": True, "message": "Notes updated successfully"}
    
    raise HTTPException(status_code=404, detail="Candidate not found")

# Interview Kit Generation
@app.post("/api/interview/generate-kit")
async def generate_interview_kit(candidate_id: str):
    """
    Generate interview kit for candidate
    """
    try:
        # Find candidate
        candidate = None
        for c in candidates_db:
            if c.id == candidate_id:
                candidate = c
                break
        
        if not candidate:
            raise HTTPException(status_code=404, detail="Candidate not found")
        
        # Get CV content (TODO: Read from file)
        cv_content = f"CV content for {candidate.name}"
        
        # Get JD for the position
        jd_text = f"Job Description for {candidate.position}"  # TODO: Get from database
        
        # Generate interview kit
        interview_kit = orchestrator.generate_interview_kit(cv_content, jd_text)
        
        return {
            "success": True,
            "candidate_id": candidate_id,
            "interview_kit": interview_kit
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating interview kit: {str(e)}")

# Health Check
@app.get("/api/health")
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
