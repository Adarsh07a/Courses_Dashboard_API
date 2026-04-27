from fastapi import FastAPI
from routes import route

app = FastAPI()
app.include_router(route)

# Run the API with: python -m uvicorn main:app --reload