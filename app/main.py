
from fastapi import FastAPI

app = FastAPI(
    title="Blog API",
    description="API для блога",
    version="1.0.0"
)


@app.get("/")
def root():
    return {"message": "Welcome to Blog API"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
