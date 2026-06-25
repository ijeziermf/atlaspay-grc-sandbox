"""Take final screenshots with longer wait time to let the data load."""
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path.home() / "Documents" / "IfeSec" / "Projects" / "atlaspay-grc-sandbox"
SHOTS = ROOT / "screenshots"
ERAMBA_URL = "https://localhost:8443"
USER, PASS = "admin", "8950Fourth"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--ignore-certificate-errors", "--no-sandbox"])
    ctx = browser.new_context(ignore_https_errors=True, viewport={"width": 1440, "height": 900})
    page = ctx.new_page()

    page.goto(ERAMBA_URL + "/login", wait_until="networkidle", timeout=60000)
    time.sleep(2)
    page.locator("input[name=login]").fill(USER)
    page.locator("input[name=password]").fill(PASS)
    page.locator("button[name=submit]").click()
    page.wait_for_selector("a:has-text('Dashboard')", timeout=30000)
    time.sleep(3)

    pages_to_capture = [
        ("/risks", "1200-risks-live.png", "Risks"),
        ("/risks/classifications", "1201-classifications-live.png", "Classifications"),
        ("/security-policies", "1202-policies-live.png", "Policies"),
        ("/business-continuity-plans", "1203-bcps-live.png", "BCPs"),
        ("/third-parties", "1204-vendors-live.png", "Vendors"),
        ("/security-incidents", "1205-incidents-live.png", "Incidents"),
    ]

    for path, fname, label in pages_to_capture:
        page.goto(ERAMBA_URL + path, wait_until="networkidle", timeout=30000)
        # Wait for table data to actually load (not just skeleton)
        try:
            page.wait_for_function(
                "() => !document.querySelector('table tbody tr.skeleton, .skeleton-row, [class*=\"skeleton\"]')",
                timeout=15000
            )
        except Exception:
            pass
        time.sleep(8)  # Extra wait for data
        page.screenshot(path=str(SHOTS / fname), full_page=True)

        # Count rows
        rows = page.evaluate("""() => {
            const trs = Array.from(document.querySelectorAll('table tbody tr')).filter(r => r.offsetWidth > 0);
            return trs.length;
        }""")
        # Also get first row text to verify it's actual data not skeleton
        first_row = page.evaluate("""() => {
            const trs = Array.from(document.querySelectorAll('table tbody tr')).filter(r => r.offsetWidth > 0 && r.innerText.trim().length > 5);
            return trs.length > 0 ? trs[0].innerText.replace(/\\n/g, ' | ').slice(0, 200) : null;
        }""")
        print(f"  {label}: visible rows={rows} first={first_row[:100] if first_row else 'NONE'}")

    browser.close()
