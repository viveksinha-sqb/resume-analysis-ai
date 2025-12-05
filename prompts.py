from typing import Dict

class PromptTemplates:
    
    SYSTEM_PROMPT = """You are an expert HR Recruiter and Talent Acquisition Specialist. 
Your goal is to analyze resumes against job descriptions to identify gaps, mismatches, and areas for verification.
You must generate specific, actionable screening questions to help a human recruiter evaluate the candidate."""

    ANALYSIS_PROMPT = """
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

Output Format:
Return a JSON object matching the following schema:
{{
  "screening_questions": [
    {{
      "question_id": 1,
      "question": "...",
      "category": "...",
      "reasoning": "...",
      "priority": "high/medium/low",
      "confidence_score": 0.0-1.0
    }}
  ],
  "analysis_summary": {{
    "issues_detected": ["..."],
    "cv_jd_match_score": 0-100
  }}
}}
"""

    @staticmethod
    def get_analysis_prompt(resume_text: str, jd_text: str) -> str:
        return PromptTemplates.ANALYSIS_PROMPT.format(
            resume_text=resume_text,
            jd_text=jd_text
        )
