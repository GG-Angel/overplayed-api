from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Config(BaseSettings):
    app_name: str = "Overplayed"
    app_description: str = "Spotify Playlist Manager"
    app_version: str = "0.1.0"

    sp_client_id: str = ""
    sp_client_secret: str = ""
    sp_scope: str = (
        "playlist-read-private playlist-modify-private playlist-modify-public"
    )


config = Config()
