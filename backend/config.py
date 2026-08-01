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

BACKEND_DIR =  Path(__file__).resolve().parent