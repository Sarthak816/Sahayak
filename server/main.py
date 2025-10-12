import uvicorn # pylint: disable=import-error
from fastapi import FastAPI  # pylint: disable=import-error
from fastapi.middleware.cors import CORSMiddleware
from routers import api

app = FastAPI()

app = FastAPI(title="JOSKI", version="1.0.0")
#app.add_middleware(
#    CORSMiddleware,
#    allow_origins=["http://localhost:3000", "http://localhost:5173", "*"],  # Add your Vue dev server @port
#    allow_credentials=True,
#    allow_methods=["*"],
#    allow_headers=["*"],
#)
app.include_router(api.router, prefix="/api/v1", tags=["API"])


@app.get("/")
async def root():
    return {"message": "Hi!"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
