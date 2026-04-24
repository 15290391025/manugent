# Security Model

ManuGent does not try to replace enterprise identity and network security. In a
real factory, authentication and authorization are usually already defined by
the customer's architecture:

- SSO / OIDC / SAML / LDAP
- API Gateway or service mesh
- VPN / zero-trust access
- MES RBAC and permission model
- OT/IT network segmentation
- SOC / SIEM audit pipelines

ManuGent's responsibility is the **Agent safety boundary** around MES tools.

## Boundary of Responsibility

| Layer | Enterprise platform owns | ManuGent owns |
|-------|--------------------------|---------------|
| Identity | SSO, IAM, user lifecycle | Optional local API token for direct demos |
| Network | VPN, gateway, firewall | No direct internet exposure assumption |
| MES authorization | MES roles and permissions | Never bypass MES connector permissions |
| Agent tools | N/A | Tool safety levels, approval boundary, audit memory |
| Audit | SIEM, enterprise retention | Structured tool-call and boundary events |

## Principles

1. **Do not let the LLM directly access arbitrary databases.**
   The LLM can only use typed MES tools.

2. **Read-heavy by default.**
   Query tools are `read_only`; action tools cross an approval boundary.

3. **No silent writes.**
   `approval` and `restricted` tools must not execute immediately inside an
   Agent response.

4. **Every tool call is auditable.**
   Tool name, params, safety level, result summary, and memory scope are stored.

5. **Session scope matters.**
   API `session_id` maps to isolated history and memory scope.

6. **Enterprise auth is pluggable.**
   The local API token is not a replacement for SSO or API Gateway.

## Optional API Token

For direct deployments or demos, set:

```bash
MANUGENT_API_TOKEN=change-me
```

Then call the API with:

```http
Authorization: Bearer change-me
```

If `MANUGENT_API_TOKEN` is empty, the guard is disabled.

## External Approval Boundary

Implemented in:

```text
src/manugent/security/approvals.py
```

The local approval queue is intentionally small and in-memory. Its purpose is
to demonstrate the contract: when an Agent recommends a production-affecting
action, the action is separated from the read-only analysis path.

ManuGent does not try to implement a universal approval engine. In real
factories this is usually already owned by MES, BPM, Lark/Feishu, ServiceNow,
or a customer-specific workflow platform. Those systems define approvers,
delegation, escalation, timeout, evidence requirements, and execution rights.

Endpoints:

```text
GET  /approvals
POST /approvals/{request_id}/decision
```

Boundary states:

- `pending`
- `approved`
- `rejected`
- `expired`

## Current Limitations

- No user/RBAC system is implemented in ManuGent.
- Approval routing and final action execution are external integration points.
- The local queue is demo-only and not meant to replace enterprise workflow.
- CORS is still permissive for demo simplicity.

## Recommended Enterprise Deployment

```text
User
→ Enterprise SSO / API Gateway
→ ManuGent API
→ MES connector with MES-scoped credentials
→ MES / ERP / QMS
```

ManuGent should receive identity/role context from the enterprise gateway, then
map that context into memory scope, tool permissions, and external approval
routing.
