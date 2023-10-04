from pyappi.api_base import app
from pyappi.block.endpoints import *
from pyappi.user.session import verify_session  
from pyappi.document.access import document_with_read_access, document_with_write_access, document_with_owner_access
from fastapi import Response
from pyappi.document.merge import server_merge
from pyappi.document.enumeration import  is_new_document, lookup_document_id
from pyappi.stats.stats import StatsRecord
from pyappi.document.delta import changes_since_dict


@app.get("/document/{id}")
@verify_session
async def get_document(id, request: Request):
    if id.startswith("!"):
        id = lookup_document_id(id[1:].split(".")[0])

    result = document_with_read_access(id, request.state.session)

    return result if result else Response(status_code=404)


@app.get("/document/delta/{id}/{tsx}")
@verify_session
async def get_delta(id, tsx, request: Request):
    if id.startswith("!"):
        id = lookup_document_id(id[1:].split(".")[0])

    result = document_with_read_access(id, request.state.session)

    return changes_since_dict(result,int(tsx)) if result else Response(status_code=404)


@app.delete("/document/{id}")
@verify_session
async def delete_document(id, request: Request):
    def handler(document):

        stats = StatsRecord(id)
        
        stats.delete()
        document.delete()

        return Response(status_code=204)

    return document_with_owner_access(id, request.state.session, handler)


@app.put("/document/{id}")
@verify_session
async def update_document(id, request: Request):
    write = await request.json()

    def handler(document):
        if document._cmt and write["_bmt"] != -1 and document._cmt != write["_bmt"]:
            return Response(status_code=409)
        
        del write["_bmt"]
            
        server_merge(document, write)

        return Response(status_code=202)

    return document_with_write_access(id, request.state.session, handler)


@app.post("/document/{id}")
async def create_document(id, request: Request):
    write = await request.json()

    def handler(document):
        if not is_new_document(document):
            return Response(status_code=409)

        if document._cmt and write["_bmt"] != -1 and document._cmt != write["_bmt"]:
            return Response(status_code=409)
        
        del write["_bmt"]
        
        # prepare_new_document(document,id)
            
        server_merge(document,write)

        return Response(status_code=202)

    return document_with_write_access(id, request.state.session, handler)
