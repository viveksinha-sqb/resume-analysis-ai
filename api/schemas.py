from typing import List, Optional
from pydantic import BaseModel, Field

class ScreeningQuestion(BaseModel):
    question_id: int
    question: str
    category: str = Field(..., description="e.g., employment_gap, skill_verification, experience_mismatch, education_validation, business_vertical")
    reasoning: str
    priority: str = Field(..., description="high, medium, low")
    confidence_score: float = Field(..., ge=0.0, le=1.0)

class AnalysisSummary(BaseModel):
    issues_detected: List[str]
    cv_jd_match_score: int = Field(..., ge=0, le=100)

class AnalysisOutput(BaseModel):
    screening_questions: List[ScreeningQuestion]
    analysis_summary: AnalysisSummary

class ResumeData(BaseModel):
    text: str
    structured_data: Optional[dict] = None

class JobDescription(BaseModel):
    text: str
    requirements: Optional[dict] = None
