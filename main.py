from fastapi import FastAPI
from endpoints import router
from config import API_HOST, API_PORT
import uvicorn

app = FastAPI(title="Veggie Vision API")

# Include the router with the ambient endpoint
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host=API_HOST, port=API_PORT)
