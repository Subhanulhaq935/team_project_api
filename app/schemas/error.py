from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    code: str = Field(..., examples=["PROJECT_NOT_FOUND"], description="Application error code")
    message: str = Field(
        ..., examples=["Project was not found."], description="Human-readable error message"
    )
    request_id: str = Field(
        ...,
        examples=["0e549acc-b55f-469e-a55c-29c34a3abab6"],
        description="Unique request tracking ID",
    )


class ErrorResponse(BaseModel):
    error: ErrorDetail
