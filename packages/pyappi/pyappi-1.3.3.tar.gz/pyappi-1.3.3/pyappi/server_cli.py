from pyappi.api_base import app,set_document_type
from pyappi.document.document import Document
from pyappi.endpoints import *
import pyappi
from colorama import Fore, Style

import uvicorn

set_document_type(Document)

def main():
    print(f"{Fore.GREEN}PYAPPI {pyappi.__version__}{Style.RESET_ALL}")
    uvicorn.run("pyappi.server_cli:app", port=8099, log_level="info")

if __name__ == "__main__":
    main()