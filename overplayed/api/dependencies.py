import time
import spotipy
from fastapi import Request
from spotipy.oauth2 import SpotifyOAuth
from overplayed.config import settings


def create_spotify_oauth(request: Request) -> SpotifyOAuth:
    return SpotifyOAuth(
        client_id=settings.spotify_client_id,
        client_secret=settings.spotify_client_secret,
        redirect_uri=request.url_for("callback"),
        scope=settings.spotify_scope,
    )


def get_token_info(request: Request) -> dict:
    token_info = request.session.get(settings.session_token_info, None)
    if not token_info:
        raise Exception("User not logged in")
    now = int(time.time())
    is_expired = token_info["expires_at"] - now < 60
    if is_expired:
        sp_oauth = create_spotify_oauth(request)
        token_info = sp_oauth.refresh_access_token(token_info["refresh_token"])
    return token_info


def get_user_id(sp: spotipy.Spotify) -> str:
    user = sp.current_user()
    if not user:
        raise ValueError("Failed to fetch user information")
    return user["id"]


def get_owned_playlists(sp: spotipy.Spotify, user_id: str) -> list:
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

        playlists = data["items"]
        if not playlists:
            break  # No more playlists to fetch

        owned_playlists.extend(filter(lambda p: p["owner"]["id"] == user_id, playlists))
        if len(playlists) < max_batch_size:
            break  # Fetched all playlists
        offset += len(playlists)

    return owned_playlists


def get_playlist_songs(sp: spotipy.Spotify, playlist_id: list) -> list:
    playlist_songs = {}
    offset = 0
    while True:
        batch = sp.playlist_items(
            playlist_id,
            limit=50,
            offset=offset,
            fields="items(added_at,track(id,name,album(name)))",
            additional_types=["track"],
        )
        if not batch:
            raise ValueError(f"Failed to fetch songs for playlist {playlist_id}")

        songs = batch["items"]
        if not songs:
            break  # No more songs to fetch

        for song in songs:
            playlist_songs[song["track"]["id"]] = song

        if len(songs) < 50:
            break  # Fetched all songs
        offset += len(songs)

    return list(playlist_songs.values())
