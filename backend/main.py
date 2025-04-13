from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import upload, transactions, categories # Import routers

app = FastAPI(
    title="Reckless Spender API",
    description="Backend API for the Reckless Spender personal finance application",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload.router)
app.include_router(transactions.router)
app.include_router(categories.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Reckless Spender API"} 