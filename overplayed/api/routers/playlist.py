from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
import spotipy
from overplayed.api.dependencies import get_owned_playlists, get_token_info

router = APIRouter()

@router.get("/")
def get_playlists(request: Request):
    try:
        token_info = get_token_info(request)
    except Exception:
        return RedirectResponse(url="/auth/login")
    sp = spotipy.Spotify(auth=token_info['access_token'])
    return get_owned_playlists(sp)
