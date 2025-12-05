import time
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        start = time.time()
        response = await call_next(request)
        duration = round((time.time() - start) * 1000, 2)

        
        log = {
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "client_ip": request.client.host,
            "duration_ms": duration,
        }

        print(log)

        
        response.headers["X-Request-ID"] = request_id
        return response
