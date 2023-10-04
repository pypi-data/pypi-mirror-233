from pyappi.api_base import app
from pyappi.block import read1, write1, is1, read2, write2, is2

from fastapi import Response, Depends, Request

async def get_body(request: Request):
    return await request.body()

@app.get("/block/{type}/{id}")
async def get_block(type, id):
    block = read1(type,id)

    return Response(status_code=404) if not block else Response(content=block, media_type='application/octet-stream')

@app.get("/block2/{type}/{id}")
async def get_block2(type, id):
    block = read2(type,id)

    return Response(status_code=404) if not block else Response(content=block, media_type='application/octet-stream')

@app.get("/is/{type}/{id}")
async def get_is(type, id):
    return is1(type,id)

@app.get("/is2/{type}/{id}")
async def get_is2(type, id):
    return is2(type,id)

@app.post("/block/{type}")
async def post_block(type, body: bytes = Depends(get_body)):
    
    id = write1(type, body)
    return {"id":id, "result":0}

@app.post("/block2/{type}/{id}")
async def post_block(type, body: bytes = Depends(get_body)):
    
    write2(type, id, body)
    return {"id":id, "result":0}