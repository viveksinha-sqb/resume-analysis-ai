import google.generativeai as genai
import json
from typing import Optional
from config import config
from schemas import AnalysisOutput
from prompts import PromptTemplates

class AIAnalyzer:
    def __init__(self):
        if not config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found in environment variables.")
        
        genai.configure(api_key=config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(
            model_name=config.GEMINI_MODEL,
            generation_config={"response_mime_type": "application/json"}
        )

    def analyze_resume(self, resume_text: str, jd_text: str) -> AnalysisOutput:
        """
        Analyzes a resume against a JD using Gemini.
        Returns structured AnalysisOutput.
        """
        prompt = PromptTemplates.get_analysis_prompt(resume_text, jd_text)
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text
            
            # Parse JSON response
            data = json.loads(response_text)
            
            # Validate against Pydantic model
            return AnalysisOutput(**data)
            
        except Exception as e:
            # TODO: Add more robust error handling and retry logic
            print(f"Error during AI analysis: {e}")
            raise e
