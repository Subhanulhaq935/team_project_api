import logging
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.core.exceptions import AppException

logger = logging.getLogger("api_logger")

def register_error_handlers(app: FastAPI):
    
    def get_request_id(request: Request) -> str:
        return getattr(request.state, "request_id", "-")

    # 1. Handle Custom Application Exceptions (ProjectNotFoundException, etc.)
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": exc.code,
                    "message": exc.message,
                    "request_id": get_request_id(request)
                }
            }
        )

    # 2. Handle standard HTTPExceptions
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        status_code_map = {
            400: "BAD_REQUEST",
            401: "UNAUTHORIZED",
            403: "FORBIDDEN",
            404: "NOT_FOUND",
            409: "CONFLICT",
            429: "TOO_MANY_REQUESTS",
            500: "INTERNAL_SERVER_ERROR"
        }
        code = status_code_map.get(exc.status_code, f"HTTP_{exc.status_code}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": code,
                    "message": str(exc.detail),
                    "request_id": get_request_id(request)
                }
            }
        )

    # 3. Handle 422 Request Validation Errors
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        errors = exc.errors()
        first_error = errors[0] if errors else {}
        loc = " -> ".join([str(l) for l in first_error.get("loc", []) if l != "body"])
        msg = first_error.get("msg", "Validation error")
        message = f"{loc}: {msg}" if loc else msg

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": message,
                    "request_id": get_request_id(request)
                }
            }
        )

    # 4. Handle 500 Unhandled Exceptions
    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled Server Error: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "An unexpected error occurred. Please try again later.",
                    "request_id": get_request_id(request)
                }
            }
        )
