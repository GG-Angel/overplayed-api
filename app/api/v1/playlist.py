from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
import spotipy
from app.dependencies import (
    fetch_user_playlists,
    fetch_playlist_tracks,
    get_token_info,
    get_user_id,
)

router = APIRouter()


@router.get("/")
def get_playlists(request: Request):
    try:
        token_info = get_token_info(request)
    except Exception:
        return RedirectResponse(url="/auth/login")
    sp = spotipy.Spotify(auth=token_info["access_token"])
    return fetch_user_playlists(sp, get_user_id(sp))


@router.get("/{playlist_id}")
def get_tracks(playlist_id: str, request: Request):
    try:
        token_info = get_token_info(request)
    except Exception:
        return RedirectResponse(url="/auth/login")
    sp = spotipy.Spotify(auth=token_info["access_token"])
    return fetch_playlist_tracks(sp, playlist_id)
