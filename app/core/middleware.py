import time
import logging
import uuid
from datetime import datetime, timezone
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from app.core.security import decode_access_token

# Logger configuration
logger = logging.getLogger("api_logger")
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 1. Check if client sent X-Request-ID header, otherwise generate new UUID
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        
        # 2. Store on request state so other middlewares & handlers can access it
        request.state.request_id = request_id
        
        # 3. Process the request
        response: Response = await call_next(request)
        
        # 4. Attach X-Request-ID to the response header
        response.headers["X-Request-ID"] = request_id
        
        return response


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()
        
        # 1. Request ID retrieve karein
        request_id = getattr(request.state, "request_id", "-")
        
        # 2. Extract user_id from Bearer token if present
        user_id = "-"
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            try:
                payload = decode_access_token(token)
                user_id = payload.get("sub", "-")
            except Exception:
                user_id = "invalid_token"
        
        # 3. Process Request
        response = await call_next(request)
        
        # 4. Calculate Duration
        duration = time.perf_counter() - start_time
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        
        # 5. Log structured message
        log_message = (
            f"{timestamp} | "
            f"request_id={request_id} "
            f"method={request.method} "
            f"path={request.url.path} "
            f"status={response.status_code} "
            f"duration={duration:.3f}s "
            f"user_id={user_id}"
        )
        logger.info(log_message)
        
        return response
