from typing import List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from config.config import config
from api.schemas import ScreeningQuestion
from utils.logger import logger

class QuestionList(BaseModel):
    questions: List[ScreeningQuestion]

class QuestionGenerator:
    def __init__(self):
        if not config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found.")
            
        self.llm = ChatGoogleGenerativeAI(
            model=config.GEMINI_MODEL,
            google_api_key=config.GEMINI_API_KEY,
            temperature=0.4 # Slightly higher creativity for questions
        )
        
        self.parser = PydanticOutputParser(pydantic_object=QuestionList)
        
        self.prompt_template = PromptTemplate(
            template="""
            Based on the following analysis of a candidate's resume against a job description, generate exactly 5 targeted screening questions.
            
            Analysis Summary:
            {analysis_summary}
            
            Issues Detected:
            {issues_detected}
            
            The questions should be:
            1. Specific to the candidate's experience and the job requirements.
            2. Professional and actionable for a recruiter.
            3. Prioritized by importance (High/Medium/Low).
            
            {format_instructions}
            """,
            input_variables=["analysis_summary", "issues_detected"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )
        
        self.chain = self.prompt_template | self.llm | self.parser

    def generate_questions(self, analysis_summary: dict, issues_detected: List[str]) -> List[ScreeningQuestion]:
        """
        Generates screening questions based on analysis results.
        """
        logger.info("Generating screening questions...")
        try:
            result = self.chain.invoke({
                "analysis_summary": str(analysis_summary),
                "issues_detected": str(issues_detected)
            })
            logger.info("Question generation completed.")
            return result.questions
        except Exception as e:
            logger.error(f"Error during question generation: {e}")
            raise e
