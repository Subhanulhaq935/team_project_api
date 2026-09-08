# 🛡️ Application Security & OWASP API Security Top 10 Matrix

This document details the security architecture, threat model, and full OWASP API Security Top 10 mitigation matrix for the **Team Project Management API**.

---

## 📊 OWASP API Security Top 10 (2023) Compliance Matrix

| OWASP Vulnerability | Threat / Description | Applied Controls in Codebase | Verification Method |
| :--- | :--- | :--- | :--- |
| **API1: Broken Object Level Authorization (BOLA)** | Accessing or modifying objects (projects, tasks) belonging to other users/tenants. | `require_project_access` dependency checks database membership for every project-scoped endpoint. | Automated test suite verifying 403 Forbidden on foreign IDs. |
| **API2: Broken Authentication** | Compromised credentials, token replay, weak password hashing. | Argon2id hashing, short-lived JWT Access Tokens (15m), rotating Refresh Tokens with reuse revocation. | Token expiration tests & invalid signature rejection tests. |
| **API3: Broken Object Property Level Authorization (BOPLA)** | Mass assignment or sensitive field exposure in request/response payloads. | Strict Pydantic schemas with `model_config = ConfigDict(extra='forbid')`, separate Request/Response DTOs. | Schema payload tests attempting to inject `is_admin` or `role`. |
| **API4: Unrestricted Resource Consumption** | DoS via unbounded pagination queries, unindexed searches, large payloads. | Enforced pagination limits (`page_size` max 100), bounded query lengths (`max_length=100`), payload limit (2MB). | Benchmark tests with `page_size=10000` verifying 422 Unprocessable Entity. |
| **API5: Broken Function Level Authorization (BFLA)** | Regular members executing administrative functions (e.g. Delete Project, Change Roles). | Role-Based Access Control (`require_roles("admin")`) applied as endpoint dependencies. | Negative authorization unit tests with Member tokens. |
| **API6: Unrestricted Access to Sensitive Business Flows** | Automated credential stuffing, rapid project/member spamming. | Flow controls on login, project creation, member role mutations, and token refresh. | Anti-automation & concurrency flow tests. |
| **API7: Server-Side Request Forgery (SSRF)** | Exploiting backend URL fetches to target loopback, internal VPCs, or cloud metadata. | `validate_url_against_ssrf` checking domain allowlist & resolving DNS against private IP subnets (`169.254.0.0/16`, `10.0.0.0/8`, etc.). | SSRF test cases attempting `http://169.254.169.254` and `http://127.0.0.1`. |
| **API8: Security Misconfiguration** | Exposing stack traces in production, permissive CORS `*`, unencrypted HTTP. | Centralized error handlers hiding traces, strict `ALLOWED_ORIGINS`, `SecurityHeadersMiddleware` (HSTS, CSP, nosniff). | Header inspection tests & mock 500 error sanitization checks. |
| **API9: Improper Inventory Management** | Undocumented endpoints, legacy API versions, shadow endpoints. | Comprehensive `docs/api-inventory.md`, version prefix `/api/v1`, OpenAPI schema governance. | Route table comparison against `docs/api-inventory.md`. |
| **API10: Unsafe Consumption of APIs** | Blindly trusting 3rd-party responses, unbounded external stream reads, untrusted certs. | `SafeAPIClient` with explicit 2s/5s timeouts, 2MB size streaming caps, mandatory TLS verify, and Pydantic validation. | Upstream failure simulation & oversized payload rejection tests. |

---

## 🔒 Security Architecture Highlights

```mermaid
graph TD
    Client[Client Request] --> WAF[Security Headers & CORS]
    WAF --> ReqID[RequestID & Logging Middleware]
    ReqID --> Router[API Router /api/v1]
    Router --> AuthCheck{JWT & RBAC Check}
    AuthCheck -- Valid --> BOLAFilter{Project Access Guard}
    AuthCheck -- Invalid --> 401[401/403 Error]
    BOLAFilter -- Authorized --> Service[Business Logic Service]
    BOLAFilter -- Unauthorized --> 403[403 Forbidden]
    Service --> SafeClient[Safe External API Client (SSRF & API10 Protected)]
    Service --> DB[(PostgreSQL Database)]

## 🧪 Security Verification & Testing Guide

Run the security test suite:

### Run all security and authorization tests

```bash
pytest -v -k "auth or security or permission or role"