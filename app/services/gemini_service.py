import google.generativeai as genai
from app.config import settings
from app.prompts import get_system_prompt


class GeminiService:
    """Service for interacting with Google Gemini API"""
    
    def __init__(self):
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    async def generate_recommendations(self, grades: str) -> str:
        """Generate course recommendations based on KCSE grades"""
        system_prompt = get_system_prompt()
        
        try:
            response = self.model.generate_content(
                f"{system_prompt}\n\nUser Grades: {grades}",
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=500,
                )
            )
            return response.text.strip()
        except Exception as e:
            print(f"Error generating recommendations: {e}")
            return "Error generating recommendations. Please try again later."


gemini_service = GeminiService()
