from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(

)

@app.get("/")
async def root():
    return {"message": "Hello, WedyAyu RAG!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)