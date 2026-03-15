from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import actual_wind, wind_forecast

app = FastAPI(title="UK Wind Forecast Monitor", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(actual_wind.router, prefix="/api")
app.include_router(wind_forecast.router, prefix="/api")

@app.get("/health")
async def health():
    return {"status": "ok"}