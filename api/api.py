from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import shutil
import os
import tempfile
from typing import Optional

from core.resume_parser import ResumeParser
from core.jd_parser import JDParser
from core.ai_analyzer import AIAnalyzer
from core.question_generator import QuestionGenerator
from api.schemas import AnalysisOutput
from utils.logger import logger

router = APIRouter()

# Initialize modules
resume_parser = ResumeParser()
jd_parser = JDParser()

try:
    ai_analyzer = AIAnalyzer()
    question_generator = QuestionGenerator()
except Exception as e:
    logger.error(f"Warning: AI Services could not be initialized: {e}")
    ai_analyzer = None
    question_generator = None

@router.post("/analyze", response_model=AnalysisOutput)
async def analyze_resume(
    resume_file: UploadFile = File(...),
    jd_text: str = Form(...)
):
    if not ai_analyzer or not question_generator:
        raise HTTPException(status_code=503, detail="AI Service unavailable (check API keys)")

    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(resume_file.filename)[1]) as tmp:
        shutil.copyfileobj(resume_file.file, tmp)
        tmp_path = tmp.name

    try:
        logger.info(f"Processing resume: {resume_file.filename}")
        
        # 1. Parse Resume
        resume_text = resume_parser.parse_file(tmp_path)
        
        # 2. Parse JD
        parsed_jd = jd_parser.parse_jd(jd_text)
        
        # 3. Analyze
        analysis_result = ai_analyzer.analyze_resume(resume_text, parsed_jd)
        
        return analysis_result

    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Cleanup temp file
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
