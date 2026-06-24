"""Capture EVERY network request Eramba makes when loading /risks/classifications.
This reveals the exact API URL pattern."""
import json, time
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path.home() / "Documents" / "IfeSec" / "Projects" / "atlaspay-grc-sandbox"
ERAMBA_URL = "https://localhost:8443"
USER, PASS = "admin", "8950Fourth"

all_traffic = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--ignore-certificate-errors", "--no-sandbox"])
    ctx = browser.new_context(ignore_https_errors=True, viewport={"width": 1440, "height": 900})
    page = ctx.new_page()

    page.on("request", lambda req: all_traffic.append({
        "type": "req", "method": req.method, "url": req.url,
        "post_data": (req.post_data[:500] if req.post_data else None),
    }))
    page.on("response", lambda resp: all_traffic.append({
        "type": "resp", "status": resp.status, "url": resp.url,
        "ct": resp.headers.get('content-type', ''),
        "body": (resp.body()[:1000].decode('utf-8', errors='ignore') if resp.body() else None),
    }))

    # Login
    page.goto(ERAMBA_URL + "/login", wait_until="networkidle", timeout=60000)
    time.sleep(2)
    page.locator("input[name=login]").fill(USER)
    page.locator("input[name=password]").fill(PASS)
    page.locator("button[name=submit]").click()
    page.wait_for_selector("a:has-text('Dashboard')", timeout=30000)
    time.sleep(3)

    # Clear and visit /risks/classifications
    all_traffic.clear()
    page.goto(ERAMBA_URL + "/risks/classifications", wait_until="networkidle", timeout=30000)
    time.sleep(5)

    print(f"=== {len(all_traffic)} requests during /risks/classifications load ===")
    for t in all_traffic:
        if t["type"] == "req":
            print(f"REQ  {t['method']} {t['url'][:120]}")
            if t.get('post_data'):
                print(f"      body: {t['post_data'][:200]}")
        else:
            print(f"RESP {t['status']} {t['url'][:120]}  ct={t.get('ct','')[:40]}")
            if t.get('body') and 'json' in t.get('ct', '').lower():
                print(f"      body: {t['body'][:200]}")

    # Save everything
    out = ROOT / "docs" / "15-all-traffic.json"
    with out.open("w") as f:
        json.dump(all_traffic, f, indent=2, default=str)
    print(f"\nSaved {len(all_traffic)} entries to {out.name}")

    browser.close()
