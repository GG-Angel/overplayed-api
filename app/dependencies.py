import time
from fastapi import Request
from spotipy.oauth2 import SpotifyOAuth
from app.config import settings

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
