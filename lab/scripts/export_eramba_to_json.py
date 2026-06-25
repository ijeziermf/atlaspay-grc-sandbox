"""
AtlasPay GRC — Eramba export.

Dumps all 32 ingested records from the live Eramba MySQL database
to a portable JSON file (data/atlaspay_eramba_export.json) with
schema-independent structure for import into CISO Assistant.
"""
import json
import subprocess
from datetime import datetime
from pathlib import Path

MYSQL_CONTAINER = "mysql"
DB = "docker"
PWD = "Your_DB_user_P@ssw0rd"
DOCKER_DIR = "/Users/ifeanyi/eramba"
OUT = Path.home() / "Documents/IfeSec/Projects/atlaspay-grc-sandbox/data" / "atlaspay_eramba_export.json"

def mysql(sql: str) -> str:
    r = subprocess.run(
        ["docker", "compose", "exec", "-T", MYSQL_CONTAINER, "mysql",
         "-udocker", f"-p{PWD}", DB, "-N", "-B", "-e", sql],
        capture_output=True, text=True, cwd=DOCKER_DIR
    )
    if r.returncode != 0:
        print(f"  SQL ERROR: {r.stderr[:200]}")
        print(f"  Query was: {sql[:150]}")
    return r.stdout

def rows(sql: str) -> list[list[str]]:
    out = mysql(sql)
    result = []
    for line in out.strip().splitlines():
        if not line.strip():
            continue
        result.append(line.split("\t"))
    return result

# --- 1. Risk Classification Types (no deleted/created/modified cols) ---
rct = rows("SELECT id, name, risk_classification_count FROM risk_classification_types ORDER BY id;")
risk_classification_types = []
for rid, name, count in rct:
    risk_classification_types.append({
        "_source_table": "risk_classification_types",
        "_eramba_id": int(rid),
        "name": name,
        "classification_count": int(count) if count and count != "NULL" else None,
    })

# --- 2. Risk Classifications (no deleted col) ---
rc = rows("SELECT id, name, value, risk_classification_type_id, created, modified FROM risk_classifications ORDER BY id;")
risk_classifications = []
for rid, name, val, type_id, c, m in rc:
    risk_classifications.append({
        "_source_table": "risk_classifications",
        "_eramba_id": int(rid),
        "name": name,
        "value": int(val) if val and val != "NULL" else None,
        "risk_classification_type_id": int(type_id) if type_id and type_id != "NULL" else None,
        "created": c,
        "modified": m,
    })

type_id_to_name = {r["_eramba_id"]: r["name"] for r in risk_classification_types}
for r in risk_classifications:
    r["_type_name"] = type_id_to_name.get(r["risk_classification_type_id"])

# --- 3. Risks (use real column names) ---
r_rows = rows("SELECT id, title, description, threats, vulnerabilities, risk_score, residual_score, residual_risk, risk_score_formula, residual_risk_formula, review, workflow_owner_id, workflow_status, created, modified FROM risks WHERE deleted = 0 ORDER BY id;")
risks = []
for row in r_rows:
    rid, title, desc, threats, vulns, rs, rsc, rr, rsf, rrf, review, owner, ws, c, m = row
    risks.append({
        "_source_table": "risks",
        "_eramba_id": int(rid),
        "title": title,
        "description": desc,
        "threats": threats,
        "vulnerabilities": vulns,
        "risk_score": float(rs) if rs and rs != "NULL" else None,
        "residual_score": int(rsc) if rsc and rsc != "NULL" else None,
        "residual_risk": float(rr) if rr and rr != "NULL" else None,
        "risk_score_formula": rsf,
        "residual_risk_formula": rrf,
        "review_date": review,
        "workflow_owner_id": int(owner) if owner and owner != "NULL" else None,
        "workflow_status": int(ws) if ws and ws != "NULL" else None,
        "created": c,
        "modified": m,
    })

# --- 4. Security Policies ---
sp_rows = rows("SELECT id, short_description, description, version, published_date, next_review_date, use_attachments, workflow_status, workflow_owner_id, created, modified FROM security_policies WHERE deleted = 0 ORDER BY id;")
security_policies = []
for row in sp_rows:
    pid, name, desc, ver, pub, nrev, att, ws, owner, c, m = row
    security_policies.append({
        "_source_table": "security_policies",
        "_eramba_id": int(pid),
        "name": name,
        "description": desc,
        "version": ver,
        "published_date": pub,
        "next_review_date": nrev,
        "use_attachments": att,
        "workflow_status": int(ws) if ws and ws != "NULL" else None,
        "workflow_owner_id": int(owner) if owner and owner != "NULL" else None,
        "created": c,
        "modified": m,
    })

# --- 5. Business Continuity Plans (use real cols) ---
bcp_rows = rows("SELECT id, title, objective, audit_metric, audit_success_criteria, launch_criteria, security_service_type_id, opex, capex, resource_utilization, regular_review, awareness_recurrence, workflow_owner_id, workflow_status, created, modified FROM business_continuity_plans WHERE deleted = 0 ORDER BY id;")
bcps = []
for row in bcp_rows:
    bid, title, obj, metric, sc, lc, sst, opex, capex, ru, review, ar, owner, ws, c, m = row
    # RTO/RPO are in the business_continuity_plan_audits join table
    bcp_text_rows = rows(f"SELECT `key`, value FROM business_continuity_plan_audits WHERE business_continuity_plan_id = {bid} AND deleted = 0;")
    bcp_meta = {k: v for k, v in bcp_text_rows}
    bcps.append({
        "_source_table": "business_continuity_plans",
        "_eramba_id": int(bid),
        "title": title,
        "objective": obj,
        "audit_metric": metric,
        "audit_success_criteria": sc,
        "launch_criteria": lc,
        "security_service_type_id": int(sst) if sst and sst != "NULL" else None,
        "opex": float(opex) if opex and opex != "NULL" else None,
        "capex": float(capex) if capex and capex != "NULL" else None,
        "resource_utilization": int(ru) if ru and ru != "NULL" else None,
        "regular_review": review,
        "awareness_recurrence": ar,
        "rto": bcp_meta.get("rto") or bcp_meta.get("RTO"),
        "rpo": bcp_meta.get("rpo") or bcp_meta.get("RPO"),
        "mto": bcp_meta.get("mto") or bcp_meta.get("MTO"),
        "workflow_owner_id": int(owner) if owner and owner != "NULL" else None,
        "workflow_status": int(ws) if ws and ws != "NULL" else None,
        "created": c,
        "modified": m,
    })

# --- 6. Third Parties (use real cols) ---
tp_rows = rows("SELECT id, name, description, third_party_type_id, security_incident_count, security_incident_open_count, service_contract_count, workflow_status, workflow_owner_id, created, modified FROM third_parties WHERE deleted = 0 ORDER BY id;")
third_parties = []
for row in tp_rows:
    tid, name, desc, tptype, sic, sioc, scc, ws, owner, c, m = row
    third_parties.append({
        "_source_table": "third_parties",
        "_eramba_id": int(tid),
        "name": name,
        "description": desc,
        "third_party_type_id": int(tptype) if tptype and tptype != "NULL" else None,
        "security_incident_count": int(sic) if sic and sic != "NULL" else 0,
        "security_incident_open_count": int(sioc) if sioc and sioc != "NULL" else 0,
        "service_contract_count": int(scc) if scc and scc != "NULL" else 0,
        "workflow_status": int(ws) if ws and ws != "NULL" else None,
        "workflow_owner_id": int(owner) if owner and owner != "NULL" else None,
        "created": c,
        "modified": m,
    })

# --- 7. Security Incidents ---
si_rows = rows("SELECT id, title, description, open_date, closure_date, workflow_status, workflow_owner_id, created, modified FROM security_incidents WHERE deleted = 0 ORDER BY id;")
security_incidents = []
for row in si_rows:
    iid, title, desc, op, cl, ws, owner, c, m = row
    security_incidents.append({
        "_source_table": "security_incidents",
        "_eramba_id": int(iid),
        "title": title,
        "description": desc,
        "open_date": op,
        "closure_date": cl,
        "workflow_status": int(ws) if ws and ws != "NULL" else None,
        "workflow_owner_id": int(owner) if owner and owner != "NULL" else None,
        "created": c,
        "modified": m,
    })

# --- 8. Risk Calculations (the actual table) ---
calc_rows = rows("SHOW TABLES LIKE 'risk_calculations';")
print(f"  risk_calculations table exists: {len(calc_rows) > 0}")

# --- Write JSON ---
export = {
    "meta": {
        "exported_at": datetime.now().isoformat(),
        "source": "Eramba CE 3.30.0",
        "source_url": "https://localhost:8443",
        "source_db": "docker",
        "schema": "AtlasPay GRC sandbox v1",
        "note": "All ingested AtlasPay records. Eramba-specific fields prefixed with _. Use the non-underscore fields for import into CISO Assistant.",
    },
    "counts": {
        "risk_classification_types": len(risk_classification_types),
        "risk_classifications": len(risk_classifications),
        "risks": len(risks),
        "security_policies": len(security_policies),
        "business_continuity_plans": len(bcps),
        "third_parties": len(third_parties),
        "security_incidents": len(security_incidents),
        "total_ingested": (len(risk_classification_types) + len(risk_classifications) + len(risks) +
                           len(security_policies) + len(bcps) + len(third_parties) + len(security_incidents)),
    },
    "risk_classification_types": risk_classification_types,
    "risk_classifications": risk_classifications,
    "risks": risks,
    "security_policies": security_policies,
    "business_continuity_plans": bcps,
    "third_parties": third_parties,
    "security_incidents": security_incidents,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
with open(OUT, "w") as f:
    json.dump(export, f, indent=2, default=str)

print(f"\nExported to: {OUT}")
print(f"Total records: {export['counts']['total_ingested']}")
for k, v in export['counts'].items():
    if k != 'total_ingested':
        print(f"  {k}: {v}")
