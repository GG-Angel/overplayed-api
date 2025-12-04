from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
import spotipy

from overplayed.api.dependencies import get_token_info
from overplayed.api.routers import auth, playlist
from overplayed.config import settings
from starlette.middleware.sessions import SessionMiddleware

session_secret_key = settings.session_secret_key
if not session_secret_key:
    raise ValueError("Session secret key is not set.")

app = FastAPI(title="Overplayed", description="Spotify Playlist Manager")

app.add_middleware(
    SessionMiddleware, secret_key=session_secret_key, session_cookie="session"
)

app.include_router(auth.router, prefix="/auth", tags=["auth"], include_in_schema=False)
app.include_router(playlist.router, prefix="/playlist", tags=["playlist"])
