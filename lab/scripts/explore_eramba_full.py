"""Find real Eramba settings + module URLs by clicking through the sidebar."""
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path.home() / "Documents" / "IfeSec" / "Projects" / "atlaspay-grc-sandbox"
SHOTS = ROOT / "screenshots"
DOCS = ROOT / "docs"
OUT = DOCS / "04-real-routes.md"
OUT.parent.mkdir(parents=True, exist_ok=True)

ERAMBA_URL = "https://localhost:8443"
USER, PASS = "admin", "8950Fourth"

OUT.write_text("# Real Eramba routes discovered via sidebar navigation\n\n")
def log(msg):
    with OUT.open("a") as f:
        f.write(f"[{time.strftime('%H:%M:%S')}] {msg}\n")
    print(msg)

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
    log(f"Logged in. URL={page.url}")

    # Enumerate all visible links
    log("\n## ALL sidebar links (live):")
    links = page.evaluate("""
        () => Array.from(document.querySelectorAll('a')).map(a => ({
            text: (a.innerText || '').trim(),
            href: a.getAttribute('href') || '',
            visible: a.getBoundingClientRect().width > 0
        })).filter(l => l.href && l.text.length < 60)
    """)
    seen = set()
    for l in links:
        key = (l['text'], l['href'])
        if key in seen:
            continue
        seen.add(key)
        log(f"  '{l['text']}' -> {l['href']}  [visible={l['visible']}]")

    # Try expanding each top-level section by clicking
    log("\n## Sidebar section expansion:")
    for section in ["Program", "Organization", "Asset Management", "Control Catalog",
                    "Risk Management", "Compliance Management", "Security Operations", "Settings"]:
        try:
            link = page.locator(f"a:has-text('{section}')").first
            link.click(timeout=2000)
            time.sleep(1)
            # Re-enumerate
            new_links = page.evaluate("""
                () => Array.from(document.querySelectorAll('a')).map(a => ({
                    text: (a.innerText || '').trim(),
                    href: a.getAttribute('href') || ''
                })).filter(l => l.href && l.text.length < 60)
            """)
            log(f"\n  After clicking '{section}':")
            for l in new_links:
                if (l['text'], l['href']) not in seen:
                    seen.add((l['text'], l['href']))
                    log(f"    '{l['text']}' -> {l['href']}")
        except Exception as e:
            log(f"  '{section}' click failed: {e}")

    # Take a screenshot showing the fully expanded sidebar
    page.locator("a:has-text('Risk Management')").first.click(timeout=2000)
    time.sleep(1)
    page.screenshot(path=str(SHOTS / "100-full-sidebar.png"), full_page=True)
    log("\nFull sidebar screenshot: 100-full-sidebar.png")

    # Try a few specific clicks to find real Settings → Risk sub-routes
    log("\n## Clicking Settings to find risk settings sub-routes:")
    page.locator("a:has-text('Settings')").first.click(timeout=3000)
    time.sleep(2)
    page.screenshot(path=str(SHOTS / "101-settings-expanded.png"), full_page=True)

    settings_links = page.evaluate("""
        () => Array.from(document.querySelectorAll('a')).map(a => ({
            text: (a.innerText || '').trim(),
            href: a.getAttribute('href') || '',
            visible: a.getBoundingClientRect().width > 0
        })).filter(l => l.href && l.visible && l.text.length < 60)
    """)
    for l in settings_links:
        log(f"  SETTINGS: '{l['text']}' -> {l['href']}")

    log("\nDone.")
    browser.close()
