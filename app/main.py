from fastapi import FastAPI

from app.api.v1 import auth, playlist
from app.core.config import config
from app.core.logging import setup_logging

setup_logging()

app = FastAPI(
    title=config.app_name,
    description=config.app_description,
    version=config.app_version,
)


app.include_router(auth.router, prefix="/auth", tags=["auth"], include_in_schema=False)
app.include_router(playlist.router, prefix="/playlists", tags=["playlists"])
