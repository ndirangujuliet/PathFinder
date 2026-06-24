from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings"""
    
    # Africa's Talking Configuration
    africastalking_username: str = Field(..., env="AFRICASTALKING_USERNAME")
    africastalking_api_key: str = Field(..., env="AFRICASTALKING_API_KEY")
    
    # Google Gemini API Configuration
    gemini_api_key: str = Field(..., env="GEMINI_API_KEY")
    
    # FastAPI Configuration
    app_name: str = Field(default="Pathfinder", env="APP_NAME")
    app_version: str = Field(default="1.0.0", env="APP_VERSION")
    debug: bool = Field(default=True, env="DEBUG")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
