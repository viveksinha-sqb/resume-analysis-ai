from typing import Optional, Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from config.config import config
from api.schemas import AnalysisOutput
from utils.logger import logger

class AIAnalyzer:
    def __init__(self):
        if not config.GEMINI_API_KEY:
            logger.error("GEMINI_API_KEY not found.")
            raise ValueError("GEMINI_API_KEY not found.")
        
        self.llm = ChatGoogleGenerativeAI(
            model=config.GEMINI_MODEL,
            google_api_key=config.GEMINI_API_KEY,
            temperature=0.2
        )
        
        self.parser = PydanticOutputParser(pydantic_object=AnalysisOutput)
        
        self.prompt_template = PromptTemplate(
            template="""
            You are an expert HR Recruiter and Talent Acquisition Specialist.
            Analyze the following Resume against the Job Description (JD).
            
            Job Description:
            {jd_text}
            
            Resume:
            {resume_text}
            
            Task:
            1. Identify employment gaps (look for date discontinuities > 3 months).
            2. Identify experience mismatches (years of experience, specific roles).
            3. Verify skills (missing critical skills required in JD).
            4. Validate education criteria.
            5. Check for business vertical alignment (e.g., if JD requires Fintech exp).
            
            {format_instructions}
            """,
            input_variables=["jd_text", "resume_text"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )
        
        self.chain = self.prompt_template | self.llm | self.parser

    def analyze_resume(self, resume_text: str, jd_text: str) -> AnalysisOutput:
        """
        Analyzes a resume against a JD using LangChain and Gemini.
        """
        logger.info("Starting AI analysis...")
        try:
            result = self.chain.invoke({
                "resume_text": resume_text,
                "jd_text": jd_text
            })
            logger.info("AI analysis completed successfully.")
            return result
        except Exception as e:
            logger.error(f"Error during AI analysis: {e}")
            raise e
