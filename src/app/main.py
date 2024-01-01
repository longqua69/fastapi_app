import uvicorn
from fastapi import FastAPI

app = FastAPI(
    title="Mini app to learn FastAPI",
    version="0.0.1",
)

@app.get("/")
async def get_homepage():
    return {"Hello": "Mom"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)