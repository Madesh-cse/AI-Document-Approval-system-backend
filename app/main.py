from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.auth import router as auth_router
from app.api.documents import router as documents_router
from app.api.dashboard import router as dashboard_router


app = FastAPI(
    title="AI Document Intelligence & Approval Platform",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(auth_router)
app.include_router(documents_router)
app.include_router(
    dashboard_router,
    prefix="/api/v1",
)


@app.get("/")
def root():
    return {
        "message": "AI Document Intelligence API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }