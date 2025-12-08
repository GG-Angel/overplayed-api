from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
import spotipy
from app.dependencies import (
    get_spotify_client,
    get_user,
    parse_datetime,
)

router = APIRouter()


@router.get("/")
def get_playlists(sp: spotipy.Spotify = Depends(get_spotify_client)):
    try:
        return get_editable_playlists(sp, get_user(sp)["id"])
    except Exception:
        return RedirectResponse(url="/auth/login")


@router.get("/{playlist_id}")
def get_tracks(playlist_id: str, sp: spotipy.Spotify = Depends(get_spotify_client)):
    try:
        return get_playlist_tracks(sp, playlist_id)
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


def get_playlist_tracks(sp: spotipy.Spotify, playlist_id: str) -> list:
    all_tracks = {}
    max_batch_size = 100
    offset = 0
    while True:
        response = sp.playlist_items(playlist_id, limit=max_batch_size, offset=offset)
        if not response:
            raise ValueError(f"Failed to fetch tracks for playlist {playlist_id}")

        # Prefer the most recently added instance of each track
        tracks: dict = response["items"]
        for track in tracks:
            track_id = track.get("track", {}).get("id")
            added_at = track.get("added_at", "1970-01-01T00:00:00Z")
            if track_id not in all_tracks or parse_datetime(
                all_tracks[track_id]["added_at"]
            ) < parse_datetime(added_at):
                all_tracks[track_id] = track

        if len(tracks) < max_batch_size:
            break
        offset += len(tracks)

    return list(all_tracks.values())
