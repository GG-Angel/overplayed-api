import os
import time
from fastapi import APIRouter, Request
from fastapi.datastructures import URL
from fastapi.responses import RedirectResponse
from spotipy.oauth2 import SpotifyOAuth
from app.config import settings

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

@router.get("/login")
def login(request: Request):
    sp_oauth = create_spotify_oauth(request)
    auth_url = sp_oauth.get_authorize_url()
    return RedirectResponse(auth_url)

@router.get("/callback")
def callback(request: Request):
    sp_oauth = create_spotify_oauth(request)
    request.session.clear()
    code = request.query_params.get("code")
    token_info = sp_oauth.get_access_token(code)
    request.session[settings.session_token_info] = token_info
    return RedirectResponse(url="/")

def create_spotify_oauth(request: Request) -> SpotifyOAuth:
    return SpotifyOAuth(
        client_id=settings.spotify_client_id,
        client_secret=settings.spotify_client_secret,
        redirect_uri=request.url_for("callback"),
        scope=settings.spotify_scope
    )

def get_token_info(request: Request):
    token_info = request.session.get(settings.session_token_info, None)
    if not token_info:
        raise Exception("User not logged in")
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if (is_expired):
        sp_oauth = create_spotify_oauth(request)
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    return token_info
