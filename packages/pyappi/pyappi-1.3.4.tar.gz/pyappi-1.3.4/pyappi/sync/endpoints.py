from pyappi.api_base import app
from pyappi.block.endpoints import *
from pyappi.user.session import verify_session
from pyappi.document.local import sync_user_local_transaction, sync_root, sync_user_local_transaction2


@app.get("/sync/status/{tsx}")
@verify_session
async def sync_status(tsx, request: Request):
    result = sync_user_local_transaction(int(tsx),request.state.session["user"])

    return result

@app.get("/sync/updates/{tsx}")
@verify_session
async def sync_updates(tsx, request: Request):
    updates, tsx = sync_user_local_transaction2(int(tsx),request.state.session["user"])

    return {"updates": updates, "tsx": tsx}

@app.get("/sync/root")
@verify_session
async def _sync_root(request: Request):
    result = sync_root(request.state.session["user"])

    return result
