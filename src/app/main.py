"""Main module of the app"""

# pylint: disable=missing-function-docstring

import uvicorn
from fastapi import FastAPI

from app.routers.users import users_router

app = FastAPI(
    title="Mini app to learn FastAPI",
    version="0.0.1",
)

app.include_router(users_router)


@app.get("/")
async def root():
    return {"Hello": "Mom"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
