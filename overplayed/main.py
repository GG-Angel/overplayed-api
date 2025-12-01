from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
import spotipy

from overplayed.api.dependencies import get_token_info
from overplayed.api.routers import auth
from overplayed.config import settings
from starlette.middleware.sessions import SessionMiddleware

session_secret_key = settings.session_secret_key
if not session_secret_key:
    raise ValueError("Session secret key is not set.")

app = FastAPI(title="Overplayed", description="Spotify Playlist Manager")

app.add_middleware(
    SessionMiddleware,
    secret_key=session_secret_key,
    session_cookie="session"
)

app.include_router(auth.router)

@app.get("/test")
def test(request: Request):
    try:
        token_info = get_token_info(request)
    except Exception as e:
        print(e)
        return RedirectResponse(url="/auth/login")
    sp = spotipy.Spotify(auth=token_info['access_token'])
    playlists_response = sp.current_user_playlists(limit=10, offset=0)
    if playlists_response and 'items' in playlists_response and playlists_response['items']:
        playlists = playlists_response['items'][0]
    else:
        return {"error": "No playlists found"}
    return {"playlists": playlists}