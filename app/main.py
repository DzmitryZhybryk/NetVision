import asyncio
from argparse import ArgumentParser

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from hypercorn.asyncio import serve
from hypercorn.config import Config

from app.api.routes import router
from app.database import db, models

parser = ArgumentParser()

parser.add_argument("--host", help=f"IPv4/IPv6 address API server would listen on", default="0.0.0.0")

parser.add_argument("--port", help=f"TCP port API server would listen on", type=int, default=8000)

app = FastAPI(docs_url="/api/v1/docs",
              redoc_url="/api/v1/redoc",
              title="some_title",
              version="0.0.1",
              description="app_name",
              swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"})

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(router, prefix="/api/v1")


@app.on_event("startup")
async def on_startup() -> None:
    async with db.engine.begin() as conn:
        await conn.run_sync(db.Base.metadata.create_all)


@app.on_event("shutdown")
async def on_shutdown() -> None:
    await db.engine.dispose()


def main() -> None:
    args = parser.parse_args()
    config = Config()
    config.bind = [f"{args.host}:{args.port}"]
    config.workers = 4
    asyncio.run(serve(app, config))  # type: ignore


if __name__ == '__main__':
    main()
