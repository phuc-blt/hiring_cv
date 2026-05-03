# /workspace/phucnt/hiring_CV/app/schemas/models.py

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


# =========================================================
# CORE REQUEST MODELS
# =========================================================

class JDRequest(BaseModel):
    """
    Input từ recruiter / hiring manager
    """
    role: str = Field(..., description="Job title, ví dụ: AI Engineer")
    company_context: str = Field(
        ...,
        description="Context về công ty, sản phẩm, domain, culture, tech stack"
    )
    seniority_level: Optional[str] = Field(
        default="mid",
        description="junior / mid / senior / lead"
    )
    employment_type: Optional[str] = Field(
        default="full-time",
        description="full-time / contract / intern"
    )


class CVUploadRequest(BaseModel):
    """
    Metadata cho CV upload
    """
    candidate_id: str
    filename: str
    source: Optional[str] = Field(
        default="upload",
        description="upload / linkedin / referral / ats"
    )


# =========================================================
# JD STRUCTURE
# =========================================================

class JDWeights(BaseModel):
    """
    Weight scoring theo role
    """
    core_ai_ml: float = 0.25
    llm_rag: float = 0.20
    projects: float = 0.20
    tools_stack: float = 0.15
    experience_years: float = 0.10
    domain_fit: float = 0.05
    communication: float = 0.05


class JobRequirement(BaseModel):
    category: str
    required_items: List[str]
    preferred_items: Optional[List[str]] = []


class JobDescription(BaseModel):
    role: str
    company_summary: str
    seniority_level: str
    responsibilities: List[str]
    requirements: List[JobRequirement]
    nice_to_have: List[str]
    tools_stack: List[str]
    success_metrics: List[str]
    weights: JDWeights


# =========================================================
# CV PARSING MODELS
# =========================================================

class CandidateSkill(BaseModel):
    name: str
    proficiency: Optional[str] = None
    years: Optional[float] = None


class CandidateProject(BaseModel):
    name: str
    description: str
    technologies: List[str]
    duration_months: Optional[int] = None
    impact: Optional[str] = None


class CandidateExperience(BaseModel):
    company: str
    title: str
    duration_months: int
    responsibilities: List[str]


class CandidateProfile(BaseModel):
    candidate_id: str
    full_name: Optional[str] = None
    email: Optional[str] = None
    total_experience_years: Optional[float] = None
    summary: Optional[str] = None
    skills: List[CandidateSkill] = []
    projects: List[CandidateProject] = []
    experiences: List[CandidateExperience] = []
    education: Optional[List[str]] = []
    certifications: Optional[List[str]] = []


# =========================================================
# RETRIEVAL MODELS
# =========================================================

class RetrievedCVChunk(BaseModel):
    chunk_id: str
    text: str
    relevance_score: float
    source_section: Optional[str] = None


class RetrievalResponse(BaseModel):
    candidate_id: str
    matched_chunks: List[RetrievedCVChunk]


# =========================================================
# SCORING MODELS
# =========================================================

class SkillScore(BaseModel):
    matched_skills: List[str]
    missing_skills: List[str]
    score: float


class ToolScore(BaseModel):
    matched_tools: List[str]
    missing_tools: List[str]
    score: float


class ProjectScore(BaseModel):
    relevant_projects: List[str]
    strengths: List[str]
    gaps: List[str]
    score: float


class ExperienceScore(BaseModel):
    years_required: Optional[float] = None
    years_actual: Optional[float] = None
    seniority_match: Optional[str] = None
    score: float


class DomainFitScore(BaseModel):
    matched_domains: List[str]
    missing_domains: List[str]
    score: float


class CommunicationScore(BaseModel):
    indicators: List[str]
    concerns: List[str]
    score: float


# =========================================================
# FINAL EVALUATION
# =========================================================

class CandidateEvaluation(BaseModel):
    candidate_id: str

    overall_score: float = Field(
        ...,
        ge=0,
        le=100,
        description="Overall candidate fit score"
    )

    skill_score: SkillScore
    tool_score: ToolScore
    project_score: ProjectScore
    experience_score: ExperienceScore
    domain_fit_score: DomainFitScore
    communication_score: CommunicationScore

    strengths: List[str]
    critical_gaps: List[str]
    hiring_recommendation: str = Field(
        ...,
        description="reject / consider / shortlist / strong_hire"
    )

    interview_questions: List[str]
    risk_flags: Optional[List[str]] = []

    explanation: Optional[str] = Field(
        default=None,
        description="Human-readable reasoning"
    )


# =========================================================
# AGGREGATED MULTI-CANDIDATE RANKING
# =========================================================

class RankedCandidate(BaseModel):
    rank: int
    candidate_id: str
    overall_score: float
    hiring_recommendation: str


class BatchEvaluationResponse(BaseModel):
    jd_role: str
    total_candidates: int
    ranked_candidates: List[RankedCandidate]


# =========================================================
# API RESPONSE WRAPPER
# =========================================================

class GenerateAndEvaluateResponse(BaseModel):
    jd: JobDescription
    candidate_evaluation: CandidateEvaluation
    metadata: Optional[Dict[str, Any]] = {}