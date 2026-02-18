from asyncio import CancelledError
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.infrastructure.database import DatabaseProvider


@asynccontextmanager
async def lifespan(app: FastAPI):
    await DatabaseProvider.init_engine()
    try:
        yield
    except CancelledError:
        pass
    finally:
        await DatabaseProvider.dispose_engine()


def create_app() -> FastAPI:
    app = FastAPI(
        title="Smart Expense Tracker",
        description="Personal finance tracking API with AI-powered analytics",
        version="0.1.0",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],  # Vite dev server
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # TODO: register routers
    # api_prefix = "/api/v1"
    # app.include_router(auth.router, prefix=api_prefix)
    # app.include_router(transactions.router, prefix=api_prefix)

    return app


app = create_app()
