from typing import Dict, Optional
import json

class JDParser:
    def __init__(self):
        pass

    def parse_jd(self, jd_content: str, is_json: bool = False) -> str:
        """
        Parse Job Description content.
        If is_json is True, tries to parse as JSON and convert to string representation.
        """
        if is_json:
            try:
                data = json.loads(jd_content)
                # Convert structured JSON back to a readable string for the LLM
                return json.dumps(data, indent=2)
            except json.JSONDecodeError:
                return jd_content
        return jd_content
