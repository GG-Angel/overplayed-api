from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from app.api.v1 import auth, playlists, top
from app.core.config import config
from app.core.logging import setup_logging

setup_logging()

app = FastAPI(
    title=config.app_name,
    description=config.app_description,
    version=config.app_version,
)

app.add_middleware(SessionMiddleware, secret_key=config.session_secret_key)


app.include_router(auth.router, prefix="/auth", tags=["auth"], include_in_schema=False)
app.include_router(playlists.router, prefix="/playlists", tags=["playlists"])
app.include_router(top.router, prefix="/top", tags=["top"])


@app.get("/")
def root():
    return RedirectResponse("/docs")
