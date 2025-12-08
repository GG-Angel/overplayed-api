from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
import spotipy

from app.dependencies import get_spotify_client


router = APIRouter()


@router.get("/")
def get_top(sp: spotipy.Spotify = Depends(get_spotify_client)):
    try:
        return get_top_tracks(sp)
    except Exception:
        return RedirectResponse(url="/auth/login")


def get_top_tracks(sp: spotipy.Spotify):
    top_tracks = {}
    time_ranges = ["short_term", "medium_term", "long_term"]
    max_limit = 50
    for time_range in time_ranges:
        response = sp.current_user_top_tracks(limit=max_limit, time_range=time_range)
        if not response or "items" not in response:
            raise ValueError(f"Failed to fetch top tracks for {time_range}")
        tracks = response.get("items", [])
        top_tracks[time_range] = tracks

    return top_tracks
