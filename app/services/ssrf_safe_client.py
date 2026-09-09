import ipaddress
import socket
from urllib.parse import urlparse

import httpx
from fastapi import HTTPException, status

# Allowed domain allowlist (only approved integrations)
APPROVED_DOMAINS = {
    "api.github.com",
    "gitlab.com",
    "slack.com",
    "hooks.slack.com",
    "api.sendgrid.com",
}

# Blocked private and link-local subnets (RFC 1918, RFC 3927, Cloud Metadata)
BLOCKED_IP_NETWORKS = [
    ipaddress.ip_network("127.0.0.0/8"),  # Loopback
    ipaddress.ip_network("10.0.0.0/8"),  # Private network
    ipaddress.ip_network("172.16.0.0/12"),  # Private network
    ipaddress.ip_network("192.168.0.0/16"),  # Private network
    ipaddress.ip_network("169.254.0.0/16"),  # Link-local / Cloud metadata (AWS/GCP/Azure)
    ipaddress.ip_network("0.0.0.0/8"),  # Broadcast / Wildcard
    ipaddress.ip_network("::1/128"),  # IPv6 loopback
    ipaddress.ip_network("fc00::/7"),  # IPv6 Unique Local Address
    ipaddress.ip_network("fe80::/10"),  # IPv6 Link-Local Address
]


def validate_url_against_ssrf(target_url: str) -> str:
    """
    Validates that a URL is safe against SSRF attacks:
    1. Only allows HTTP/HTTPS schemes.
    2. Enforces approved domain allowlist.
    3. Resolves DNS and blocks private/loopback/cloud metadata IP ranges.
    """
    parsed = urlparse(target_url)

    # 1. Validate Scheme
    if parsed.scheme.lower() not in ("http", "https"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid URL scheme. Only HTTP and HTTPS are permitted.",
        )

    hostname = parsed.hostname
    if not hostname:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid URL: Hostname missing."
        )

    # 2. Validate Domain Allowlist
    if hostname.lower() not in APPROVED_DOMAINS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Domain '{hostname}' is not on the approved external services allowlist.",
        )

    # 3. DNS Resolution & IP Range Verification (Prevents DNS Rebinding & Private IP routing)
    try:
        ip_addresses = socket.getaddrinfo(
            hostname, parsed.port or (443 if parsed.scheme == "https" else 80)
        )
        for addr_info in ip_addresses:
            ip_str = addr_info[4][0]
            ip_obj = ipaddress.ip_address(ip_str)

            for blocked_net in BLOCKED_IP_NETWORKS:
                if ip_obj in blocked_net:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Access to private, local, or cloud metadata network addresses is strictly forbidden.",
                    )
    except socket.gaierror as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to resolve destination hostname.",
        ) from err

    return target_url


async def fetch_approved_external_resource(target_url: str) -> dict:
    """
    Safely executes an external GET request with SSRF controls, timeouts, and size limits.
    """
    validated_url = validate_url_against_ssrf(target_url)

    # API10 controls: timeout, max size limit, TLS validation
    async with httpx.AsyncClient(verify=True, timeout=5.0) as client:
        try:
            response = await client.get(validated_url, follow_redirects=False)

            # Limit response payload size to 1MB
            if len(response.content) > 1_000_000:
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail="External response exceeded maximum size limit of 1MB.",
                )

            return {
                "status_code": response.status_code,
                "data": response.json()
                if "application/json" in response.headers.get("content-type", "")
                else response.text[:500],
            }
        except httpx.TimeoutException as exc:
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="External service request timed out.",
            ) from exc
        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Error communicating with external service: {exc!s}",
            ) from exc
