# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import language_routes, dialect_routes, province_routes, municipality_routes, phrase_routes, provincelanguage_routes, municipalitylanguage_routes, delicacy_routes, tourist_spot_routes, statistics_routes
from flask import Flask, send_from_directory


app = Flask(__name__)

@app.route('/')
def serve_frontend():
    return send_from_directory('../frontend', 'index.html')

async def serve_frontend():
    with open("../frontend/index.html") as f:
        return HTMLResponse(content=f.read())

if __name__ == '__main__':
    app.run()

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

# Routes
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
