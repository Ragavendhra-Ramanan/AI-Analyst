# main.py
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import your router
from .router import rag_file_upload, generate_deal_note, generate_benchmark
from vertex_config import init_vertex

app = FastAPI(title="Async File Processor API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    init_vertex()


app.include_router(rag_file_upload.router, prefix="/api", tags=["Upload"])
app.include_router(generate_deal_note.router, prefix="/api", tags=["Generate"])
app.include_router(generate_benchmark.router, prefix="/api", tags=["Benchmark"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
