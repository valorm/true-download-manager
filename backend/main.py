from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer

from auth import router as auth_router
from database import init_db
import models  # noqa: F401

app = FastAPI(
    title="True Download Manager",
    description="A modern, feature-rich download manager with multi-threaded downloads and media extraction support",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OAuth2 scheme for JWT authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.on_event("startup")
async def startup():
    init_db()

@app.get("/")
async def root():
    return {"message": "Welcome to True Download Manager API"}

# Import and include routers here after they are created
app.include_router(auth_router, tags=["auth"])
# app.include_router(downloads.router, prefix="/downloads", tags=["downloads"])
# app.include_router(websocket.router, tags=["websocket"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
