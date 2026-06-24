"""Use Playwright to capture the actual AJAX request Eramba sends when we click Add+Save.
This is the surest way to find the exact API contract."""
import json
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path.home() / "Documents" / "IfeSec" / "Projects" / "atlaspay-grc-sandbox"
SHOTS = ROOT / "screenshots"
ERAMBA_URL = "https://localhost:8443"
USER, PASS = "admin", "8950Fourth"

captured_requests = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--ignore-certificate-errors", "--no-sandbox"])
    ctx = browser.new_context(ignore_https_errors=True, viewport={"width": 1440, "height": 900})
    page = ctx.new_page()

    # Capture ALL requests to /api/ or /crud/ paths
    def on_request(req):
        if '/api/' in req.url or '/crud/' in req.url or 'crud=' in req.url:
            captured_requests.append({
                "method": req.method,
                "url": req.url,
                "headers": dict(req.headers),
                "post_data": req.post_data[:500] if req.post_data else None,
            })

    def on_response(resp):
        if '/api/' in resp.url or '/crud/' in resp.url or 'crud=' in resp.url:
            try:
                body = resp.body()
                captured_requests.append({
                    "type": "response",
                    "method": resp.request.method,
                    "url": resp.url,
                    "status": resp.status,
                    "body": body[:1000].decode('utf-8', errors='ignore') if body else None,
                })
            except Exception:
                pass

    page.on("request", on_request)
    page.on("response", on_response)

    # Login
    page.goto(ERAMBA_URL + "/login", wait_until="networkidle", timeout=60000)
    time.sleep(2)
    page.locator("input[name=login]").fill(USER)
    page.locator("input[name=password]").fill(PASS)
    page.locator("button[name=submit]").click()
    page.wait_for_selector("a:has-text('Dashboard')", timeout=30000)
    time.sleep(3)

    # Visit /risks/classifications
    page.goto(ERAMBA_URL + "/risks/classifications", wait_until="networkidle", timeout=30000)
    time.sleep(3)
    print("=== At /risks/classifications ===")
    print(f"  Captured so far: {len(captured_requests)}")
    for r in captured_requests[-5:]:
        print(f"  {r}")

    # Click Actions dropdown
    page.locator("a.dropdown-toggle:has-text('Actions')").first.click()
    time.sleep(1)

    # Click Add
    page.locator(".dropdown-menu a:has-text('Add')").first.click()
    page.wait_for_load_state("networkidle", timeout=15000)
    time.sleep(3)

    print(f"\n=== After Add click ===")
    print(f"  Captured: {len(captured_requests)}")
    for r in captured_requests[-5:]:
        print(f"  {r.get('method', '?')} {r.get('url', '?')[:100]}")

    # Save everything captured to a file
    out = ROOT / "docs" / "13-captured-api-calls.json"
    with out.open("w") as f:
        json.dump(captured_requests, f, indent=2, default=str)
    print(f"\nSaved {len(captured_requests)} captured requests to {out.name}")

    browser.close()
