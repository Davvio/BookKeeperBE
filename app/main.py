from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base, engine
from app.routes import auth, trades, users

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "https://bookkeeperfe.onrender.com",  # Render frontend
    "http://localhost:5173",              # Vite dev
    "http://localhost:3000",              # (optional) alt dev ports
]

# 1️⃣ CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2️⃣ Routers
app.include_router(auth.router)
app.include_router(trades.router, prefix="/trades", tags=["Trades"])
app.include_router(users.router)
