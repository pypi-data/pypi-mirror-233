from pyappi.api_base import app, get_document_type
from fastapi import Request, Response
from pyappi.user.session import parse_session, verify_session, generate_token
from pyappi.document.enumeration import is_new_document, prepare_new_document

@app.get("/user/token/{id}")
@verify_session
async def generate_user_token(id, request: Request):
    return {"token":generate_token(request.state.session)}

@app.post("/user/create/{id}")
async def create_user(id, request: Request):
    raw_session = request.query_params._list[0][0]
    session = parse_session(raw_session)
    body = await request.json()
    
    document_id = f'user.{id}'

    with get_document_type()(document_id, session["user"]) as doc:
        if not is_new_document(doc):
            return Response(status_code=409)
        
        # prepare_new_document(doc,document_id)
        
        doc._perm[id] = "owner"
        doc.auth.challenge = session["challenge"]
        doc.auth.enc_pri_key = body.get("enc_pri_key","")
        doc["~public"].identity.pub_key = body.get("pub_key","")
        doc["~public"].profile = body.get("profile",{})

    with get_document_type()(f'subs.{id}', session["user"]) as doc:
        if len(doc._perm):
            return Response(status_code=409)
        
        doc._perm[id] = "owner"

    return Response(status_code=201)

@app.post("/user/validate/{id}")
@verify_session
async def validate_user(id, request: Request):
    return Response(status_code=202)