import time
import spotipy
from fastapi import Request
from spotipy.oauth2 import SpotifyOAuth
from app.core.config import config


def create_spotify_oauth(request: Request) -> SpotifyOAuth:
    return SpotifyOAuth(
        client_id=config.sp_client_id,
        client_secret=config.sp_client_secret,
        redirect_uri=request.url_for("callback"),
        scope=config.sp_scope,
    )


def get_spotify_client(request: Request) -> spotipy.Spotify:
    token_info = get_token_info(request)
    return spotipy.Spotify(auth=token_info["access_token"])


def get_token_info(request: Request) -> dict:
    token_info = request.session.get("token_info", None)
    if not token_info:
        raise Exception("User not logged in")
    now = int(time.time())
    is_expired = token_info["expires_at"] - now < 60
    if is_expired:
        sp_oauth = create_spotify_oauth(request)
        token_info = sp_oauth.refresh_access_token(token_info["refresh_token"])
    return token_info


def get_user(sp: spotipy.Spotify) -> dict:
    user = sp.me()
    if not user:
        raise ValueError("Failed to fetch user info")
    return user
