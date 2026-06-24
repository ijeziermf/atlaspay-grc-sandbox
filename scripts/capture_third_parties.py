"""Capture the actual AJAX response when loading the third-parties page."""
import json, time
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path.home() / "Documents" / "IfeSec" / "Projects" / "atlaspay-grc-sandbox"
ERAMBA_URL = "https://localhost:8443"
USER, PASS = "admin", "8950Fourth"

traffic = []
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--ignore-certificate-errors", "--no-sandbox"])
    ctx = browser.new_context(ignore_https_errors=True, viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    page.on("response", lambda r: traffic.append({
        "url": r.url, "status": r.status, "ct": r.headers.get("content-type", ""),
        "body": r.body()[:2000].decode("utf-8", errors="ignore") if r.body() else None
    }) if ("/api/" in r.url or "/crud/" in r.url or "/system-api/" in r.url or "third-parties" in r.url) else None)

    page.goto(ERAMBA_URL + "/login", wait_until="networkidle", timeout=60000)
    time.sleep(2)
    page.locator("input[name=login]").fill(USER)
    page.locator("input[name=password]").fill(PASS)
    page.locator("button[name=submit]").click()
    page.wait_for_selector("a:has-text('Dashboard')", timeout=30000)
    time.sleep(3)

    traffic.clear()
    page.goto(ERAMBA_URL + "/third-parties", wait_until="networkidle", timeout=30000)
    time.sleep(8)

    # Print all non-static-asset traffic
    print("=== Responses to /third-parties page ===")
    for t in traffic:
        if 'vue_assets' in t['url'] or 'eramba-assets' in t['url']:
            continue
        print(f"\n{t['status']} {t['url'][:140]}")
        if t.get('ct', '').startswith('application/json') and t.get('body'):
            try:
                j = json.loads(t['body'])
                print(f"  JSON keys: {list(j.keys()) if isinstance(j, dict) else type(j).__name__}")
                if isinstance(j, dict) and 'data' in j:
                    data = j['data']
                    if isinstance(data, dict) and 'items' in data:
                        print(f"  data.items count: {len(data['items'])}")
                    elif isinstance(data, list):
                        print(f"  data list count: {len(data)}")
                    elif isinstance(data, dict):
                        print(f"  data keys: {list(data.keys())[:10]}")
                print(f"  body[:500]: {t['body'][:500]}")
            except Exception:
                print(f"  body[:500]: {t['body'][:500]}")
        elif t.get('ct', '').startswith('text/html') and t.get('body'):
            print(f"  HTML[:200]: {t['body'][:200]}")

    out = ROOT / "docs" / "19-third-parties-traffic.json"
    with out.open("w") as f:
        json.dump(traffic, f, indent=2)
    browser.close()
