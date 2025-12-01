import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    spotify_client_id: str = os.getenv("SPOTIFY_CLIENT_ID")
    spotify_client_secret: str = os.getenv("SPOTIFY_CLIENT_SECRET")
    session_secret_key: str = os.getenv("SESSION_SECRET_KEY")

    spotify_scope: str = "playlist-read-private playlist-modify-private playlist-modify-public"
    session_token_info: str = "token_info"

settings = Settings()