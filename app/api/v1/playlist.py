from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
import spotipy
from app.dependencies import (
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


# TODO: cache results for 1-6 hours until user applies playlist changes on frontend
