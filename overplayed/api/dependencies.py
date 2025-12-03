import time
from fastapi.responses import RedirectResponse
import spotipy
from fastapi import Query, Request
from spotipy.oauth2 import SpotifyOAuth
from overplayed.config import settings

def create_spotify_oauth(request: Request) -> SpotifyOAuth:
    return SpotifyOAuth(
        client_id=settings.spotify_client_id,
        client_secret=settings.spotify_client_secret,
        redirect_uri=request.url_for("callback"),
        scope=settings.spotify_scope
    )

def get_token_info(request: Request) -> dict:
    token_info = request.session.get(settings.session_token_info, None)
    if not token_info:
        raise Exception("User not logged in")
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if (is_expired):
        sp_oauth = create_spotify_oauth(request)
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    return token_info

def get_owned_playlists(sp: spotipy.Spotify) -> list:
    user = sp.current_user()
    if not user:
        raise ValueError("Failed to fetch user information")

    owned_playlists = []
    max_batch_size = 50
    offset = 0
    while True:
        data = sp.current_user_playlists(limit=max_batch_size, offset=offset)
        if not data:
            raise ValueError("Failed to fetch playlists")
        
        playlists = data['items']
        if not playlists:
            break # No more playlists to fetch
        
        owned_playlists.extend(filter(lambda p: p['owner']['id'] == user['id'], playlists))
        offset += len(playlists)
        if len(playlists) < max_batch_size:
            break # Fetched all playlists

    return owned_playlists