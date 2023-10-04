from pyappi.api_base import app
from fastapi import Request
from pyappi.user.session import verify_session
from pyappi.stats.stats import update_viewing_sesison


@app.post("/stats/view/{id}/{session}/{secret}")
@verify_session
async def view(id, session, secret, request: Request):
    stats = update_viewing_sesison(id, request.state.session["user"])

    return {"session":0, "secret": 0, "stats": stats}