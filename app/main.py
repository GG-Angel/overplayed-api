import os
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from .routers import auth
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

secret_key = os.getenv("SESSION_SECRET_KEY")
if not secret_key:
    raise RuntimeError("Environment variable 'SESSION_SECRET_KEY' is not set")

app.add_middleware(
    SessionMiddleware,
    secret_key=secret_key,
)

app.include_router(auth.router)

@app.get("/")
def index():
  return {"message": "Hello, World!"}

@app.get("/test")
def test(request: Request):
    try:
        token_info = auth.get_token_info(request)
        return {"logged_in": True, "token_info": token_info}
    except Exception as e:
        print(e)
        return RedirectResponse(url="/auth/login")