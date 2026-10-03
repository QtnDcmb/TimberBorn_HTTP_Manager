import os
from urllib.parse import quote

import httpx
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/game", tags=["timberborn"])

# Where the game's HTTP API listens. Override with the TIMBERBORN_URL env var.
GAME_URL = os.getenv("TIMBERBORN_URL", "http://localhost:8080")


async def call_game(path: str):
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            r = await client.get(f"{GAME_URL}{path}")
    except httpx.RequestError as e:
        raise HTTPException(502, f"Cannot reach Timberborn at {GAME_URL}: {e!r}")
    if r.status_code >= 400:
        raise HTTPException(r.status_code, f"Game returned: {r.text}")
    try:
        return r.json()
    except ValueError:
        return {"response": r.text}


@router.get("/levers")
async def list_levers():
    return await call_game("/api/levers")


@router.get("/levers/{name}")
async def get_lever(name: str):
    return await call_game(f"/api/levers/{quote(name)}")


@router.post("/levers/{name}/on")
async def switch_on(name: str):
    return await call_game(f"/api/switch-on/{quote(name)}")


@router.post("/levers/{name}/off")
async def switch_off(name: str):
    return await call_game(f"/api/switch-off/{quote(name)}")
