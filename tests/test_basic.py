import pytest
from fastapi.testclient import TestClient
from main import app
from core.resume_parser import ResumeParser
from core.jd_parser import JDParser
from api.schemas import AnalysisOutput, ScreeningQuestion, AnalysisSummary
import os
from unittest.mock import MagicMock, patch

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Resume Analysis AI API is running"}

def test_resume_parser_txt():
    parser = ResumeParser()
    # Create dummy txt file
    with open("dummy.txt", "w") as f:
        f.write("John Doe\nSoftware Engineer")
    
    try:
        text = parser.parse_file("dummy.txt")
        assert "John Doe" in text
        assert "Software Engineer" in text
    finally:
        if os.path.exists("dummy.txt"):
            os.remove("dummy.txt")

def test_jd_parser():
    parser = JDParser()
    jd_text = "Software Engineer required. Python, FastAPI."
    parsed = parser.parse_jd(jd_text)
    assert parsed == jd_text

@patch("api.api.ai_analyzer")
@patch("api.api.question_generator")
def test_analyze_endpoint_mock(mock_qg, mock_ai):
    # Mock AI Analyzer response
    mock_ai.analyze_resume.return_value = AnalysisOutput(
        screening_questions=[],
        analysis_summary=AnalysisSummary(
            issues_detected=[],
            cv_jd_match_score=80
        )
    )
    
    # Create dummy resume file
    with open("dummy_resume.txt", "w") as f:
        f.write("Resume Content")
        
    try:
        with open("dummy_resume.txt", "rb") as f:
            response = client.post(
                "/analyze",
                files={"resume_file": ("dummy_resume.txt", f, "text/plain")},
                data={"jd_text": "JD Content"}
            )
        
        assert response.status_code == 200
        data = response.json()
        assert "screening_questions" in data
        assert "analysis_summary" in data
    finally:
        if os.path.exists("dummy_resume.txt"):
            os.remove("dummy_resume.txt")
