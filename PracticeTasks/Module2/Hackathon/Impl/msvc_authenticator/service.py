from fastapi import FastAPI, HTTPException, Request
from datetime import datetime, timedelta
import uuid
from model import SessionData
import settings


# TODO: Redis shall be used
sessions = {}

# TODO: make it configurable by admin?
TOKEN_LIFETIME_MINUTES = 60

msvc_authenticator = FastAPI(title="Authenticating Microservice", version="1.0.0", description="Provides bearing authentication.")
msvc_authenticator.mount(settings.path_base, msvc_authenticator)

def create_session(username: str) -> str:
    token = str(uuid.uuid4())
    expires_at = datetime.now() + timedelta(minutes=TOKEN_LIFETIME_MINUTES)
    sessions[token] = SessionData(username=username, expires_at=expires_at)
    return token

def validate_token(token: str) -> SessionData:
    session = sessions.get(token)
    if not session or session.expires_at < datetime.now():
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return session

@msvc_authenticator.post("/auth/login", tags=["Authenticator"], summary="Create bearing token")
def login(username: str):
    # TODO: RBAC must be used or the actual authentication
    token = create_session(username)
    return {"token": token}

@msvc_authenticator.post("/auth/validate", tags=["Authenticator"], summary="Validate bearing token")
def validate(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization header")
    token = auth_header.split(" ")[1]
    session = validate_token(token)
    return {"success": True, "username": session.username}
