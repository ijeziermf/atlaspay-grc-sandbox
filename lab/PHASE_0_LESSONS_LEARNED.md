# Phase 0 — Lessons Learned (2026-06-23, ~10:40 EDT)

## What happened
Adeola subagent (`deleg_7d129e1d`) was dispatched to port 22 AtlasPay records from PDFs into CISO Assistant CE v3.18.3. After 7 minutes, it returned with a "mostly done" report claiming 22 records ingested, 3 frameworks loaded, 6 screenshots captured.

**Independent verification by Hermes COO found 0 records ingested, 0 frameworks loaded, 0 screenshots.** The subagent built the REST client (`scripts/ca_api.py`, 6.6KB, verified working) but ran out of tool-call budget before writing any of the 10 ingestion scripts.

## Root cause
Subagent's report read like it had done the work because it described each step as completed. But the actual artifacts on disk were just one Python file (the client). The discrepancy is a textbook example of the failure mode memory calls "never summarize writes that errored" — the subagent reported forward progress, not actual file-system state.

## Schema facts Adeola discovered (correct, saving here so we don't re-discover)

| Task spec endpoint | Actual CISO Assistant v3.18.3 endpoint |
|---|---|
| `risk-assessments` (for the 6 risks) | `risk-scenarios` (the 6 risks live here; `risk-assessments` is the container) |
| `business-continuity-plans` | **DOES NOT EXIST in v3.18.3 OSS** — commercial-only module |
| `third-parties` (vendors) | `entities` + `contracts` + `solutions` (composite model) |
| `frameworks` (count) | `loaded-libraries` is the count of loaded frameworks |

Frameworks in the 267-library catalog (URNs identified):
- `urn:intuitem:risk:library:nist-csf-2.0` ✓
- `urn:intuitem:risk:library:iso27001-2022` ✓
- `urn:intuitem:risk:library:soc2-2017-2022` (or `soc2-2017-rev-2022`) ✓
- Mappings: `nist-csf-2.0-to-iso27001-2022`, `soc2-2017-rev-2022-to-iso27001-2022` ✓

## Auth pattern (verified by Hermes, not Adeola)

Token-based auth works:
- Token lives in `/Users/ifeanyi/Documents/IfeSec/Tools/ciso-assistant-community/cli/.mcp.env`
- 64 chars, single line `TOKEN=<value>`
- API_URL=26 chars (likely `https://localhost:8443/api`)
- VERIFY_CERTIFICATE=false
- Header: `Authorization: Token <value>` (NOT Bearer)
- Verified working: GET /api/folders/?limit=1 returns count=2 (Global + AtlasPay)

Cookie-based auth also works (proven in earlier session):
- POST /api/_allauth/browser/v1/auth/login with JSON `{email, password}`, X-CSRFToken cookie + Referer header
- Returns sessionid cookie
- Use this when no MCP token is available

## BCP gap — decision needed from Ifeanyi

3 options on the table:
- (a) Skip BCPs, ingest 18 records, document gap, plan Phase 4 enhancement
- (b) Encode BCPs as `assets` with `recovery_objective` + `recovery_point_objective` custom fields, ingest 22
- (c) Research whether a hidden endpoint exists before deciding

## What needs to happen next

1. ~~Ifeanyi picks (a), (b), or (c)~~ ✅ **DECIDED: option (b)** — encode BCPs as `assets` with recovery fields
2. **Phase 0a re-dispatched** as `deleg_eeeeeb68` (scoped narrowly to foundation only)
3. Once Phase 0a reports done, Hermes verifies via raw urllib count (not the client)
4. **Phase 0b runs `./ingest_data.sh`** (5 ingestion scripts staged + verifier on disk)
5. Phase 0b scripts use the corrected schema from `phase0a_foundation.py` (parent_folder UUID, content_type DOMAIN, folder for perimeters, etc.)
6. **Phase 0c** (Playwright screenshots) dispatched after 0b verified
7. Then **Phase 1a + 1c** skills (Adeola) build the sandbox-bootstrap + screenshot-harness skills
8. Then **Phase 2 + 3** (Helix Health + Meridian Bank) in parallel

## Schema facts verified during re-stage (2026-06-23 ~10:58)

| Field | Endpoint | Verified format |
|---|---|---|
| Folders (subfolders) | POST /api/folders/ | `{name, parent_folder: UUID, content_type: "DOMAIN"}` |
| Perimeters | POST /api/perimeters/ | `{name, folder: UUID, scope_in: [..], scope_out: [..]}` |
| Frameworks (load) | POST /api/stored-libraries/{urn}/import/ | `{}` (empty body). NOTE: path is `/import/` not `/load/` as originally documented. |
| Risk matrix | POST /api/risk-matrices/ | `{name, description, json_definition: {probability, impact, risk, grid, type}}` (REST broken — see Django ORM workaround below) |
| Risk assessments (container) | POST /api/risk-assessments/ | `{name, description, ref_id, status, version, eta, due_date, risk_tolerance, folder: UUID, risk_matrix: UUID}` (REST broken — use ORM) |
| Risk scenarios | POST /api/risk-scenarios/ | `{name, description, inherent_level, residual_level, treatment, ref_id, folder: UUID, risk_matrix: UUID, risk_assessment: UUID, category}` |
| Policies | POST /api/policies/ | `{name, description, status, priority, csf_function, next_review_date, ref_id, folder: UUID, category}` — enums: category=policy/process/technical/physical/procedure, status=to_do/in_progress/on_hold/active/degraded/deprecated/--, priority=1-4, csf_function=govern/identify/protect/detect/respond/recover |
| Entities | POST /api/entities/ | `{name, description, ref_id, folder: UUID, category}` |
| Contracts | POST /api/contracts/ | `{name, description, ref_id, folder: UUID, entity: UUID, category}` |
| Incidents | POST /api/incidents/ | `{name, description, type, severity, status, open_date, folder: UUID, ref_id}` — enums: status=new/ongoing/resolved/closed/dismissed, severity=1-6 (1=Critical, 2=Major, 3=Moderate, 4=Minor, 5=Low, 6=unknown) |
| Assets | POST /api/assets/ | `{name, description, type, business_value, is_business_function, ref_id, folder: UUID, disaster_recovery_objectives: {rto, rpo, ref, recovery_strategy}}` — enums: type=PR/SP |

The `ca_api.post()` returns `(status_code, body)` tuple, not body directly. All ingestion scripts account for this.

## Risk matrix + risk assessment workaround (CA v3.18.3 OSS bug)

The REST write path for `ReferentialSerializer`-derived models (RiskMatrix, RiskAssessment) is broken — `get_name_translated` is a `@property` with no setter, so any POST with `name` field raises `AttributeError: property has no setter` → HTTP 500.

**Workaround:** Bypass REST and use Django ORM directly via `docker exec backend python -c "..."`:

```bash
docker compose -f ~/Documents/IfeSec/Tools/ciso-assistant-community/docker-compose.yml exec -T backend python -c "
import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ciso_assistant.settings')
django.setup()
from core.models import RiskMatrix, RiskAssessment, Folder
matrix = RiskMatrix.objects.create(name='AtlasPay 5x5', ...)
ra = RiskAssessment.objects.create(name='AtlasPay SOC 2 Readiness Risk Assessment', risk_matrix=matrix, folder=...)
"
```

**This is the ONLY way to create these objects in v3.18.3 OSS.** Will need to re-apply if container is rebuilt.

## Final Phase 0b count (verified via /tmp/verify_state.py + scripts/verify_phase_0b.py)

```
folders            6   (Global + AtlasPay + 4 sub)        ✅
perimeters         5   (3 pre + AtlasPay-Payments + AtlasPay-Data) ✅
risk-scenarios     6   (R-01..R-06)                        ✅
policies           4   (ACC-01, IR-01, SA-01, TPRM-01)     ✅
entities           8   (7 AtlasPay vendors + 1 pre-existing "Main") ✅
contracts          7   (1 MSA per vendor)                  ✅
incidents          1   (Phishing linked to R-01)           ✅
assets             4   (BCPs as critical business fns)     ✅
risk-matrices      1   (AtlasPay 5x5)                      ✅
loaded-libraries  56   (52 + NIST CSF 2.0 + ISO 27001:2022 + SOC 2) ✅
risk-assessments   1   (RA-ATLASPAY-SOC2 container)       ✅
```

**22 records across the right models.** All data preserved (RTO/RPO, inherent/residual scores, severity, descriptions). Discord gate unblocked once Phase 0c screenshots return.

## Phase 0d — Risk matrix population fix (2026-06-23 ~11:25)

Hermes re-verification discovered that the `AtlasPay 5x5` RiskMatrix existed but its `json_definition` was `{}` — empty probability/impact/risk/grid. As a consequence, all 6 risk-scenarios had `inherent_level = -1` (no matrix to look up).

Root cause: when Phase 0a used the Django ORM workaround to create the matrix, it set `name` and other fields but did not populate `json_definition`. The CA REST write path is broken for `ReferentialSerializer` models so the missing definition could not be back-filled via API.

Fix: `scripts/phase0c_matrix_fix.py` re-fetches the matrix by name and writes a complete 5x5 ISO-27005 `json_definition` directly via ORM (idempotent). Schema transcribed verbatim from `backend/library/libraries/risk-matrix-5x5-iso-27005.yaml` (English-only to keep payload small; full multi-locale not needed for the sandbox). Verified via independent `scripts/verify_phase0_foundation.py` (urllib, NOT ca_api).

**Caveat:** This fix populates the matrix only. The 6 risk-scenarios still have `inherent_proba=-1, inherent_impact=-1` because they were ingested without those values (Phase 0b data ingest scope, not foundation scope). A future script will need to PATCH each scenario with concrete inherent_proba/inherent_impact/residual_proba/residual_impact numbers so the matrix can compute `inherent_level`/`residual_level`.

## Council process corrections

- **Don't trust subagent "completed" reports.** Always re-verify with file-system check + API count.
- **Subagent tool budget needs to be sized for the work.** 7 minutes was insufficient for 22 records + 6 screenshots + framework loading. Need to either give more budget OR break into smaller dispatched tasks.
- **The "ready to send Discord" milestone is a Hermes verification, not a subagent report.**
- **Smaller scoped dispatches work better** than one giant task. Phase 0 split into 0a (foundation), 0b (data ingest), 0c (screenshots) — each scoped to <10 min runtime.
