from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.api import router as api_router
from utils.logger import logger

app = FastAPI(title="Resume Analysis AI")

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

@app.get("/")
async def root():
    logger.info("Health check endpoint called.")
    return {"message": "Resume Analysis AI API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
