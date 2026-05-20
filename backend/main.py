# /products/main.py
# FastAPI app entrypoint for product API routing.
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from products.apis.products_apis import app as api_app

app = api_app

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Run server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
