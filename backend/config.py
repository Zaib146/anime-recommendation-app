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
    
    # Environment variables are useful because configuration can change between your PC, Mac, and AWS, while your application code remains the same. Sensitive values such as future database credentials also stay out of committed source code.
    DATABASE_URL: str = "anime_app.db"
    
    # ALLOWED_ORIGINS is another "setting" we create (it's technically a variable / field of Settings). It will be a list of strings. It's a list since we may eventually have multiple origins (urls). An origin is the combination of protocol + domain/hostname + port
    # http — protocol, localhost — hostname, 5173 — Vite development-server port. The backend will eventually pass this setting to FastAPI’s CORS middleware.
    # Field is a Pydantic function that lets us configure how this settings field behaves. Here, we use Field to tell Pydantic how to produce the default list.
    # A default factory is a function that Pydantic calls whenever it needs the default value. Instead of storing one shared list directly, Pydantic creates a fresh list for each Settings object. This is safer because lists are mutable—they can be changed.
    # A lambda is a short, unnamed function. lambda: ["http://localhost:5173"] means “When called, create and return a new list containing http://localhost:5173.”
    # if no external value is supplied, this settings.ALLOWED_ORIGINS will contain ["http://localhost:5173"]. Later, the backend/.env file could override the default - ALLOWED_ORIGINS=["http://localhost:5173","https://yourdomain.com"]
    # Pydantic reads that JSON-formatted list and converts it into a real Python list[str]
    
    # “Create an ALLOWED_ORIGINS setting that must be a list of strings. If no environment-specific value is provided, use a newly created list that permits the local Vite frontend.”
    ALLOWED_ORIGINS: list[str] = Field(
        default_factory=lambda: ["http://localhost:5173"]
    )
    
    # DATABASE_URL and ALLOWED_ORIGINS describe what settings your application has
    # model_config describes how Pydantic should load and handle those settings.
    # SettingsConfigDict helps construct those Pydantic-specific instructions correctly.
    
    # model_config is the standard name Pydantic looks for when configuring a model. Here the "model" is the Settings class. When Settings() creates the settings object, Pydantic uses model_config to know things like where to find .env; how to decode it; how to handle extra entries.
    # model_config means “configuration for the Pydantic model class.”
    # SettingsConfigDict is a class imported from pydantic_settings that creates the configuration dictionary in the format Pydantic expects
    
    # SettingsConfigDict(...) produces configuration instructions roughly resembling:
    # {
    # "env_file": BACKEND_DIR / ".env",
    # "env_file_encoding": "utf-8",
    # "extra": "ignore",
    # }    
    # Those instructions are assigned to the special model_config variable. When Pydantic processes your Settings class, it recognizes that name and uses those instructions.
    
    # In plain english, the below model_config block is: “When creating a Settings object, look for configuration in backend/.env, read it as UTF-8, and ignore any entries that this settings class does not define.”
    
    model_config = SettingsConfigDict(
        
        # This is the line that tells Pydantic where to find the .env file. It does not perform the override by itself. It configures Pydantic to read backend/.env when this later runs: settings = Settings()
        # At that moment, Pydantic chooses each value according to this priority:
            # 1. Real operating-system/AWS environment variable
            # 2. Value in backend/.env
            # 3. Default written in the Settings class

        env_file=BACKEND_DIR / ".env",
        
        # Read the .env file using standard UTF-8 text encoding.
        env_file_encoding="utf-8",
        
        # If .env contains a variable that has no corresponding field in Settings, ignore it instead of raising an error.
        extra="ignore",
    )
    
settings = Settings()