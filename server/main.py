from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import os
from api import router as api_router

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
app.mount(
    "/static",
    StaticFiles(directory=os.path.join(__location__, "static")),
    name="static",
)

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    # return FileResponse(os.path.join(__location__, "static", "favicon.ico"))
    
    return ''

# Include the api router
app.include_router(api_router, prefix="/api", tags=["api"])

@app.get("/")
async def read_root():
    return FileResponse(os.path.join(__location__, "static", "index.html"))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9090)