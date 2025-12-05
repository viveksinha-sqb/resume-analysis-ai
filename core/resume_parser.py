from typing import Optional
import os
# import pypdf
# import docx

class ResumeParser:
    def __init__(self):
        pass

    def parse_file(self, file_path: str) -> str:
        """
        Extract text from a resume file (PDF, DOCX, TXT).
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext == '.pdf':
            return self._parse_pdf(file_path)
        elif ext in ['.docx', '.doc']:
            return self._parse_docx(file_path)
        elif ext == '.txt':
            return self._parse_txt(file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")

    def _parse_pdf(self, file_path: str) -> str:
        text = ""
        try:
            from pypdf import PdfReader
            reader = PdfReader(file_path)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        except ImportError:
            return "Error: pypdf not installed."
        except Exception as e:
            return f"Error parsing PDF: {str(e)}"
        return text

    def _parse_docx(self, file_path: str) -> str:
        text = ""
        try:
            import docx
            doc = docx.Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"
        except ImportError:
            return "Error: python-docx not installed."
        except Exception as e:
            return f"Error parsing DOCX: {str(e)}"
        return text

    def _parse_txt(self, file_path: str) -> str:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
