from __future__ import annotations

import os
import sys
from typing import Optional
from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
import uvicorn

app = FastAPI()

ROOT = os.path.dirname(__file__)
OCRS_FILE = os.path.join(ROOT, 'ocrs.html')


@app.get('/', response_class=HTMLResponse)
def index():
    """Serve the ocrs.html demo page if present."""
    if os.path.exists(OCRS_FILE):
        return FileResponse(OCRS_FILE, media_type='text/html')
    return HTMLResponse('<h1>ocrs.html not found</h1>', status_code=404)

def run(port: Optional[int] = None, host: str = '0.0.0.0') -> None:
    if port is None:
        port = int(os.environ.get('PORT', '8000'))

    print(f'Starting FastAPI app on http://{host}:{port} (serving {OCRS_FILE})')
    uvicorn.run('04_fastapi_demo:app', host=host, port=port, log_level='info', reload=False)


if __name__ == '__main__':
    _port: Optional[int] = None
    if len(sys.argv) > 1:
        try:
            _port = int(sys.argv[1])
        except ValueError:
            print('Usage: python 04_fastapi_demo.py [port]', file=sys.stderr)
            sys.exit(1)
    run(port=_port)
