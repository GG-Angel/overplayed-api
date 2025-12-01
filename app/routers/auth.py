import os
from fastapi import APIRouter

router = APIRouter(
  prefix='/auth',
  tags=['auth']
)

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
SPOTIFY_SCOPES = "playlist-read-private playlist-modify-private playlist-modify-public"

@router.get("/login")
def login():
    return {"message": "Authentication endpoint"}