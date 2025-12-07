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
        return get_editable_playlists(sp, get_user(sp)["id"])
    except Exception:
        return RedirectResponse(url="/auth/login")


def get_editable_playlists(sp: spotipy.Spotify, user_id: str) -> list:
    all_editable_playlists = []
    max_batch_size = 50
    offset = 0
    while True:
        response = sp.current_user_playlists(limit=max_batch_size, offset=offset)
        if not response:
            raise ValueError("Failed to fetch playlists")

        # Filter playlists that are owned by the user or are collaborative
        playlists: dict = response["items"]
        editable_playlists = filter(
            lambda p: p.get("owner", {}).get("id") == user_id
            or p.get("collaborative", False),
            playlists,
        )
        all_editable_playlists.extend(editable_playlists)

        if len(playlists) < max_batch_size:
            break
        offset += len(playlists)

    return all_editable_playlists
