"""Click the page-level Settings button on /risks and see what URL it goes to."""
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

    # Login
    page.goto(ERAMBA_URL + "/login", wait_until="networkidle", timeout=60000)
    time.sleep(2)
    page.locator("input[name=login]").fill(USER)
    page.locator("input[name=password]").fill(PASS)
    page.locator("button[name=submit]").click()
    page.wait_for_selector("a:has-text('Dashboard')", timeout=30000)
    time.sleep(3)

    # Go to Asset Risks
    page.goto(ERAMBA_URL + "/risks", wait_until="networkidle", timeout=30000)
    time.sleep(3)
    print(f"Risks page URL: {page.url}")

    # Find the Settings button (page-level, not sidebar)
    settings_btn = page.locator("button[aria-label='Settings']").first
    if settings_btn.is_visible(timeout=3000):
        print("Clicking Settings button (page-level)...")
        settings_btn.click()
        time.sleep(2)
        page.screenshot(path=str(SHOTS / "120-after-settings-click.png"), full_page=True)
        print(f"  URL after click: {page.url}")

        # Find any sub-options that appeared
        new_links = page.evaluate("""
            () => Array.from(document.querySelectorAll('a, button')).map(el => ({
                tag: el.tagName.toLowerCase(),
                text: (el.innerText || '').trim().slice(0, 80),
                href: el.getAttribute('href') || '',
                visible: el.getBoundingClientRect().width > 0
            })).filter(el => el.visible && el.text.length > 0 && el.text.length < 80)
        """)
        for l in new_links[:30]:
            if 'classif' in l['text'].lower() or 'calcul' in l['text'].lower() or \
               'appetite' in l['text'].lower() or 'risk' in l['text'].lower():
                print(f"  <{l['tag']}> '{l['text']}' -> {l['href']}")

        # If we got a dropdown, dump all visible items
        print("\nAll visible items on settings panel:")
        for l in new_links[:50]:
            print(f"  <{l['tag']}> '{l['text']}' -> {l['href']}")
    else:
        print("Settings button NOT visible on /risks")

    browser.close()
