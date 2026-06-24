# CISO Assistant v3.18.3 — Verified Schema Facts

**Verified:** 2026-06-23 by Adeola subagent + Hermes COO independent re-check
**Source:** `~/Documents/IfeSec/Tools/ciso-assistant-community/`
**Live at:** `https://localhost:8443`

## Endpoint mapping (task spec → actual)

| Task spec endpoint | Actual CA v3.18.3 endpoint | Notes |
|---|---|---|
| `risk-assessments` (for the 6 risks) | **`risk-scenarios`** | risk-assessments is the container; scenarios hold the actual risks |
| `business-continuity-plans` | **DOES NOT EXIST in OSS** | Commercial-only module. Encode as `assets` with `recovery_objective` + `recovery_point_objective` custom fields, OR skip. |
| `third-parties` (vendors) | **`entities`** + `contracts` + `solutions` | Composite model — vendor = entity + linked contracts + linked solutions |
| `frameworks` count | `loaded-libraries` count | Frameworks are "loaded libraries" in v3.18.3 |

## Auth patterns

### Option A: Cookie (session-based)
```
POST /api/_allauth/browser/v1/auth/login
Headers: X-CSRFToken: <cookie>, Referer: https://localhost:8443/
Body: {"email":"ijeziermf@gmail.com","password":"8950Fourth"}
Returns: sessionid cookie
```

### Option B: Token (PAT-based, what MCP uses)
```
GET /api/folders/?limit=1
Headers: Authorization: Token <64-char-token>
```
Token lives in `/Users/ifeanyi/Documents/IfeSec/Tools/ciso-assistant-community/cli/.mcp.env`
Format: `TOKEN=<64 chars>`, `API_URL=https://localhost:8443/api`, `VERIFY_CERTIFICATE=false`

**Note:** Header is `Authorization: Token <value>`, NOT `Authorization: Bearer <value>`. Bearer returns 401.

### Curl note
**Curl to localhost hangs in shell on macOS** (sandboxed shell environment issue). Use Python `urllib.request` with `ssl._create_unverified_context()` instead. See `scripts/ca_api.py` for working pattern.

## Framework library URNs (verified in 267-library catalog)

| URN | Loaded? |
|---|---|
| `urn:intuitem:risk:library:nist-csf-2.0` | No — needs `POST /api/stored-libraries/{urn}/load/` |
| `urn:intuitem:risk:library:iso27001-2022` | No — needs load |
| `urn:intuitem:risk:library:soc2-2017-rev-2022` | No — needs load |
| Mapping: `nist-csf-2.0-to-iso27001-2022` | Available |
| Mapping: `soc2-2017-rev-2022-to-iso27001-2022` | Available |

Currently 52 libraries loaded by default (likely framework skeletons + bundled content). AtlasPay-specific frameworks not yet loaded.

## Baseline counts (as of 2026-06-23 ~10:40 EDT)

| Model | Count | Notes |
|---|---|---|
| folders | 2 | Global + AtlasPay (AtlasPay pre-exists from prior session) |
| perimeters | 3 | 2 real + 1 test |
| entities | 1 | "Main" |
| risk-scenarios | 0 | |
| risk-assessments | 0 | (container, empty) |
| risk-matrices | 0 | |
| policies | 0 | |
| incidents | 0 | |
| frameworks | 0 | (loaded-libraries has 52, but no frameworks loaded into AtlasPay) |
| stored-libraries | 267 | (catalog, available) |
| assets | 0 | |
| users | 1 | (admin only) |

## Pitfalls discovered (2026-06-23)

1. **CISO Assistant uses `risk-scenarios` for individual risks, NOT `risk-assessments`.** The task spec's endpoint names assumed Eramba v3.30.0 names.
2. **`business-continuity-plans` endpoint absent in v3.18.3 OSS.** Commercial-only.
3. **Vendors are composite:** `entities` (vendor record) + `contracts` (linked) + `solutions` (linked). Single POST to /third-parties won't work.
4. **Frameworks load via URN, not ID.** The 267-library catalog has URNs; load via `POST /api/stored-libraries/{urn}/load/`.
5. **Curl hangs in this shell environment** — use Python urllib.
6. **Subagent "completed" reports need independent verification.** Adeola claimed 22 records ingested in 7 minutes, actual was 0 records + 1 client script only. Always `ls -la` files + re-GET API counts before declaring done.

## Working REST client (already written, verified)

`/Users/ifeanyi/Documents/IfeSec/Projects/atlaspay-grc-sandbox/scripts/ca_api.py` (6,659 bytes)
- Reads TOKEN + API_URL from `.mcp.env`
- `get`, `post`, `patch`, `count`, `all_results`, `find_by`, `post_if_absent` helpers
- Handles DRF pagination (strips `/api` then re-prepends for relative `next` URLs)
- Unverified SSL for self-signed cert
- Verified working: `count('folders')` returns 2

This client is ready to drive all 10 ingestion scripts.
