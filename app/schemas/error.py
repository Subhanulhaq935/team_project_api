from pydantic import BaseModel, Field

class ErrorDetail(BaseModel):
    code: str = Field(..., example="PROJECT_NOT_FOUND", description="Application error code")
    message: str = Field(..., example="Project was not found.", description="Human-readable error message")
    request_id: str = Field(..., example="0e549acc-b55f-469e-a55c-29c34a3abab6", description="Unique request tracking ID")

class ErrorResponse(BaseModel):
    error: ErrorDetail
