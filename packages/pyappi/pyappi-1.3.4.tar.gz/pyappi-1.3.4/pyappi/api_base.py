from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

description = """"""
version = "1.3.4"

@asynccontextmanager
async def lifespan(app: FastAPI):
    from pyappi.stats.stats import session_cleanup_interval, use_session_interval

    use_session_interval()

    #print("startup")

    yield
    #print("shutdown")


    if session_cleanup_interval:
        session_cleanup_interval.stop()

app = FastAPI(title="pyappi", description=description, version=version, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

document_type = None
def set_document_type(dt):
    global document_type

    document_type = dt

def get_document_type():
    return document_type