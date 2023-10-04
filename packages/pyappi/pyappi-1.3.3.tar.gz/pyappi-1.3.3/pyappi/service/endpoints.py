from pyappi.api_base import app
from fastapi import Request
from pyappi.service.session import verify_service
from pyappi.stats.stats import update_viewing_sesison
from pyappi.events.events import read_events, read_cursor


@app.get("/service/read_events/{tsx}")
@verify_service
async def read(tsx, request: Request):
    return read_events(int(tsx))


@app.get("/service/cursor")
@verify_service
async def cursor(request: Request):
    return read_cursor()