import os
from fastapi import APIRouter, Request
from fastapi.datastructures import URL
from fastapi.responses import RedirectResponse
from spotipy.oauth2 import SpotifyOAuth

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
SPOTIFY_SCOPES = "playlist-read-private playlist-modify-private playlist-modify-public"
SESSION_TOKEN_INFO = "token_info"

@router.get("/login")
def login(request: Request):
    sp_oauth = create_spotify_oauth(request.url_for("callback"))
    auth_url = sp_oauth.get_authorize_url()
    return RedirectResponse(auth_url)

@router.get("/callback")
def callback(request: Request):
    sp_oauth = create_spotify_oauth(request.url_for("callback"))
    request.session.clear()
    code = request.query_params.get("code")
    token_info = sp_oauth.get_access_token(code)
    request.session[SESSION_TOKEN_INFO] = token_info
    return 'redirect'


def create_spotify_oauth(redirect_uri: URL) -> SpotifyOAuth:
    return SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=redirect_uri,
        scope=SPOTIFY_SCOPES
    )

def get_token_info(request: Request):
    token_info = request.session.get(SESSION_TOKEN_INFO, None)
    if not token_info:
        raise Exception("User not logged in")
