"""Login to CISO Assistant and take a screenshot of the dashboard."""
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path.home() / "Documents/IfeSec/Projects/atlaspay-grc-sandbox"
SHOTS = ROOT / "screenshots"
URL = "https://localhost:8443"
USER, PASS = "ijeziermf@gmail.com", "8950Fourth"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--ignore-certificate-errors", "--no-sandbox"])
    ctx = browser.new_context(ignore_https_errors=True, viewport={"width": 1440, "height": 900})
    page = ctx.new_page()

    page.goto(URL + "/login", wait_until="domcontentloaded", timeout=30000)
    time.sleep(3)
    page.screenshot(path=str(SHOTS / "2000-ca-login.png"), full_page=True)

    # Login
    page.locator("input[name=email], input[type=email]").first.fill(USER)
    page.locator("input[type=password]").first.fill(PASS)
    page.locator("button[type=submit]").first.click()
    page.wait_for_url("**/home**", timeout=30000)
    time.sleep(5)
    page.screenshot(path=str(SHOTS / "2001-ca-dashboard.png"), full_page=True)

    # Check what menu items are present
    nav_items = page.evaluate("""() => {
        const items = Array.from(document.querySelectorAll('nav a, aside a, [role=link]'))
          .map(a => a.innerText.trim())
          .filter(t => t.length > 0 && t.length < 40);
        return [...new Set(items)];
    }""")
    print("Nav items found:", nav_items[:30])

    browser.close()
