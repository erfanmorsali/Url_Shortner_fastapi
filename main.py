from fastapi import FastAPI
from api.api import api_router
import uvicorn


app = FastAPI()


app.include_router(api_router, tags=["API_V1"])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)