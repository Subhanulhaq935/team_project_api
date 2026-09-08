import httpx
from pydantic import BaseModel, ValidationError
from typing import Type, TypeVar
from fastapi import HTTPException, status

T = TypeVar("T", bound=BaseModel)

class SafeAPIClient:
    """
    OWASP API10 compliant external API consumer:
    - Explicit Connect (2s) & Read (5s) Timeouts
    - Enforced TLS / Certificate Verification
    - Strict Response Body Size Limit (max 2MB)
    - Pydantic Schema Parsing (treats all external data as untrusted)
    """

    MAX_RESPONSE_BYTES = 2 * 1024 * 1024  # 2MB

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            verify=True,  # Mandatory TLS Certificate Validation
            timeout=httpx.Timeout(5.0, connect=2.0),
            headers={"User-Agent": "TeamProjectAPI-Integration/1.0"}
        )

    async def get(self, endpoint: str, response_schema: Type[T]) -> T:
        try:
            # Stream response to enforce size limits before buffering into memory
            async with self.client.stream("GET", endpoint) as response:
                if response.status_code >= 400:
                    raise HTTPException(
                        status_code=status.HTTP_502_BAD_GATEWAY,
                        detail=f"Upstream service returned error code: {response.status_code}"
                    )

                content = bytearray()
                async for chunk in response.aiter_bytes():
                    content.extend(chunk)
                    if len(content) > self.MAX_RESPONSE_BYTES:
                        raise HTTPException(
                            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                            detail="Upstream response payload exceeded maximum allowed limit (2MB)."
                        )

                # Parse JSON
                try:
                    import json
                    json_data = json.loads(content.decode("utf-8"))
                except Exception:
                    raise HTTPException(
                        status_code=status.HTTP_502_BAD_GATEWAY,
                        detail="Upstream service returned non-JSON payload."
                    )

                # Validate data against Pydantic schema
                try:
                    return response_schema.model_validate(json_data)
                except ValidationError as err:
                    raise HTTPException(
                        status_code=status.HTTP_502_BAD_GATEWAY,
                        detail=f"Upstream payload validation failed schema expectations: {err.errors()}"
                    )

        except httpx.TimeoutException:
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="Upstream request timed out."
            )
        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Network error communicating with upstream service: {str(exc)}"
            )

    async def close(self):
        await self.client.aclose()
