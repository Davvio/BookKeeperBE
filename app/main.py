import os

from alembic import command
from alembic.config import Config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base
from app.core.database import engine, SessionLocal
from app.routes import auth, trades, users
from app.routes.item_values import router as values_router
from app.routes.items import router as items_router
from app.routes.structure_settings import router as settings_router
from app.services.seed import seed_minimal

#Base.metadata.create_all(bind=engine)

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
app.include_router(items_router)
app.include_router(settings_router)
app.include_router(values_router)

def run_migrations():
    cfg = Config("alembic.ini")
    command.upgrade(cfg, "head")

@app.on_event("startup")
def on_startup():
    # 1) Run migrations first (only when enabled via env var)
    if os.getenv("RUN_MIGRATIONS") == "1":
        run_migrations()

    # 2) Seed AFTER migrations
    db = SessionLocal()
    try:
        seed_minimal(db)
    finally:
        db.close()