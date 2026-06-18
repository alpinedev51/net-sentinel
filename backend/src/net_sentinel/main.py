# App factory, mounts middleware, hooks, routers
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from net_sentinel.controllers.router import api_router
from net_sentinel.hooks.lifespan import lifespan

app = FastAPI(
    title="Net-Sentinel",
    description="A security auditing service",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
)

app.include_router(api_router)
