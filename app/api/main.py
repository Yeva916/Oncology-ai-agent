from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import analyze, demo, health, debug


app = FastAPI(title="Onco Agent API")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze.router, prefix="/api")
app.include_router(demo.router, prefix="/api")
app.include_router(health.router, prefix="/api")
app.include_router(debug.router, prefix="/api")


@app.get("/")
def root():
    return {"message": "Onco Agent API"}
