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


def get_spotify_client(request: Request) -> spotipy.Spotify:
    token_info = get_token_info(request)
    return spotipy.Spotify(auth=token_info["access_token"])


def get_user(sp: spotipy.Spotify) -> dict:
    user = sp.me()
    if not user:
        raise ValueError("Failed to fetch user info")
    return user


def fetch_user_playlists(sp: spotipy.Spotify, user_id: str) -> list:
    owned_playlists = []
    max_batch_size = 50
    offset = 0
    while True:
        data = sp.current_user_playlists(limit=max_batch_size, offset=offset)
        if not data:
            raise ValueError("Failed to fetch playlists")

        playlists = data["items"]
        owned_playlists.extend(filter(lambda p: p["owner"]["id"] == user_id, playlists))

        if len(playlists) < max_batch_size:
            break  # Fetched all playlists
        offset += len(playlists)

    return owned_playlists


def fetch_playlist_tracks(sp: spotipy.Spotify, playlist_id: str) -> list:
    playlist_tracks = {}
    max_batch_size = 100
    offset = 0
    while True:
        data = sp.playlist_items(
            playlist_id,
            offset=offset,
            limit=max_batch_size,
            fields="items(added_at,track(id,name,album(name))),total",
        )
        if not data:
            raise ValueError("Failed to fetch playlist items")

        tracks = list(map(lambda item: item["track"], data["items"]))
        for track in tracks:
            if track["id"] not in playlist_tracks:
                playlist_tracks[track["id"]] = track  # Deduplicate tracks by ID

        if len(tracks) < max_batch_size:
            break
        offset += len(tracks)
        time.sleep(1)

    return list(playlist_tracks.values())


# TODO: cache results for 1-6 hours until user applies playlist changes on frontend
