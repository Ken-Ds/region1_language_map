from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.routes import language_routes, dialect_routes, province_routes, municipality_routes, phrase_routes, provincelanguage_routes, municipalitylanguage_routes, delicacy_routes, tourist_spot_routes, statistics_routes

app = FastAPI(
    title="Language Mapping API",
    description="API for comparing phrases and regional language data.",
    version="1.0"
)

# Allow frontend requests (adjust if deploying)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (like your frontend HTML)
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Serve the HTML (index.html) at root URL
@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    with open("frontend/index.html", "r") as f:
        return HTMLResponse(content=f.read())

# Routes (your existing FastAPI routes)
app.include_router(dialect_routes.router)
app.include_router(language_routes.router)
app.include_router(phrase_routes.router)
app.include_router(province_routes.router)
app.include_router(provincelanguage_routes.router)
app.include_router(municipality_routes.router)
app.include_router(municipalitylanguage_routes.router)
app.include_router(delicacy_routes.router)
app.include_router(tourist_spot_routes.router)
app.include_router(statistics_routes.router)
