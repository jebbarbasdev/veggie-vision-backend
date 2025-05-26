from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from endpoints import router
from config import API_HOST, API_PORT
import uvicorn

app = FastAPI(title="Veggie Vision API")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the router with the ambient endpoint
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host=API_HOST, port=API_PORT)
