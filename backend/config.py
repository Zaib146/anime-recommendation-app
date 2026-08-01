# pathlib is part of Python’s standard library. Path provides a reliable way to construct file paths on Windows, macOS, and Linux. We will use it to identify the exact location of the backend folder so that Pydantic can reliably find: backend/.env
# Project runs on PC, Mac and Linux (when deployed to AWS). Path handles the operating-system differences for us.
from pathlib import Path

# Field lets us configure how a Pydantic field’s default value is created. need it to use Field later
from pydantic import Field

# A regular Pydantic BaseModel validates data passed directly to it. BaseSettings adds configuration-source support. BaseSettings tells Pydantic - “These fields represent application configuration and may be populated from environment variables or a .env file.”
# SettingsConfigDict - This configures how the Settings class behaves, including which .env file to read (env_file), which text encoding to use (env_file_encoding), what to do with unrelated variables in that file (extra)
from pydantic_settings import BaseSettings, SettingsConfigDict

# Given C:\anime-recommendation-app\backend\config.py, this sets BACKEND_DIR to C:\anime-recommendation-app\backend. BACKEND_DIR gives the program a dependable reference point for locating files that belong inside the backend folder.

# __file__ is a special Python variable containing the path of the current file: C:\anime-recommendation-app\backend\config.py
# Path(__file__) converts the path string into a Path object, which provides convenient, cross-platform path operations
# .resolve() produces the complete absolute path and resolves relative components such as ..
# .parent selects the directory containing that file: C:\anime-recommendation-app\backend

BACKEND_DIR =  Path(__file__).resolve().parent

# This creates our own class called Settings, based on Pydantic’s BaseSettings. The Settings class serves as the definition—or schema—for the backend’s configuration. It states: Which settings exist, What type each setting must have,
# What defaults should be used, Where local settings can be loaded from
class Settings(BaseSettings):
    
    # DATABASE_URL inside Settings is your Python settings field (not a default setting, it's a field / variable we create). We treat it as 1 "setting" inside this class. DATABASE_URL outside Python is the corresponding environment-variable name.
    # if the corresponding environment-variable name exists, Pydantic Settings connects the two. "anime_app.db" in the class is the fallback if neither external source provides a value. str says DATABASE_URL must be of type string.
    DATABASE_URL: str = "anime_app.db"