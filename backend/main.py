from fastapi import FastAPI
from core.database import db
from graph.schema import initialize_schema

from api.nmap import router as nmap_router
from api.analysis import router as analysis_router
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

app = FastAPI(title="Attack Path Engine API")

# Serve the frontend
import os
os.makedirs("static", exist_ok=True)
app.mount("/dashboard", StaticFiles(directory="static", html=True), name="static")

@app.get("/")
def read_root():
    return RedirectResponse(url="/dashboard/index.html")

app.include_router(nmap_router, prefix="/api/nmap", tags=["Nmap"])
app.include_router(analysis_router, prefix="/api/analysis", tags=["Analysis"])

@app.on_event("startup")
def startup_event():
    # Attempt to initialize schema on startup
    try:
        initialize_schema()
    except Exception as e:
        print(f"Could not initialize Neo4j schema (is Neo4j running?): {e}")

@app.on_event("shutdown")
def shutdown_event():
    db.close()

@app.get("/")
def read_root():
    return {"message": "Attack Path Engine API is running. Neo4j is ready for data."}

@app.get("/health")
def health_check():
    return {"status": "ok"}
