from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import messages, upload

app = FastAPI(title="BeeBot AI Chat API (Stateless)")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "BeeBot Stateless AI API is running"}

# Include only necessary routers
app.include_router(messages.router, prefix="/chat", tags=["messages"])
app.include_router(upload.router, prefix="/upload", tags=["upload"])
