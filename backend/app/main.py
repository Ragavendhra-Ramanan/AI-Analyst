# main.py
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import your router
from router import process_raw_pitches
from vertex_config import init_vertex

app = FastAPI(title="Async File Processor API", version="1.0.0")

# -------------------------
# Enable CORS
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change ["*"] to a specific domain list in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    init_vertex()


# -------------------------
# Include Routers
# -------------------------
app.include_router(process_raw_pitches.router, prefix="/api", tags=["Upload"])


# -------------------------
# Entry point
# -------------------------
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
