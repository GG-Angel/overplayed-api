from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
import spotipy
from app.dependencies import (
    fetch_user_playlists,
    fetch_playlist_tracks,
    get_spotify_client,
    get_user,
)

router = APIRouter()


@router.get("/")
def get_playlists(sp: spotipy.Spotify = Depends(get_spotify_client)):
    try:
        return fetch_user_playlists(sp, get_user(sp)["id"])
    except Exception:
        return RedirectResponse(url="/auth/login")


@router.get("/{playlist_id}")
def get_tracks(playlist_id: str, sp: spotipy.Spotify = Depends(get_spotify_client)):
    try:
        return fetch_playlist_tracks(sp, playlist_id)
    except Exception:
        return RedirectResponse(url="/auth/login")
