"""Find and click the actual page-level Settings dropdown on /risks."""
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

    page.goto(ERAMBA_URL + "/risks", wait_until="networkidle", timeout=30000)
    time.sleep(3)

    # List all buttons on the page with their position
    btns = page.evaluate("""
        () => Array.from(document.querySelectorAll('button')).filter(el => el.getBoundingClientRect().width > 0).map(el => {
            const r = el.getBoundingClientRect();
            return {
                text: (el.innerText || el.value || '').trim().slice(0, 30),
                ariaLabel: el.getAttribute('aria-label') || '',
                x: Math.round(r.x), y: Math.round(r.y),
                w: Math.round(r.width), h: Math.round(r.height),
                cls: (el.className || '').toString().slice(0, 80),
                id: el.id || ''
            };
        })
    """)
    print(f"All buttons ({len(btns)}):")
    for b in btns:
        print(f"  '{b['text']}' aria='{b['ariaLabel']}' pos=({b['x']},{b['y']}) {b['w']}x{b['h']} cls={b['cls'][:60]}")

    # The Settings button is at top of page near title. Try clicking it.
    settings = page.locator("button[aria-label='Settings']").first
    if settings.count() > 0:
        # Get its position
        box = settings.bounding_box()
        print(f"\nSettings button box: {box}")
        # Click it
        settings.click()
        time.sleep(2)
        page.screenshot(path=str(SHOTS / "610-settings-clicked.png"), full_page=True)

        # Look for any new visible dropdown menus
        items = page.evaluate("""
            () => {
                const items = [];
                document.querySelectorAll('a, button, [role="menuitem"]').forEach(el => {
                    const r = el.getBoundingClientRect();
                    if (r.width === 0) return;
                    const text = (el.innerText || el.value || '').trim();
                    if (text && text.length > 0 && text.length < 80) {
                        items.push({
                            tag: el.tagName.toLowerCase(),
                            text: text,
                            href: el.getAttribute('href') || '',
                            visible: true,
                            x: Math.round(r.x), y: Math.round(r.y)
                        });
                    }
                });
                return items;
            }
        """)
        print(f"\nItems visible after click ({len(items)}):")
        for i in items:
            if 'classification' in i['text'].lower() or 'appetite' in i['text'].lower() or \
               'calculation' in i['text'].lower() or 'treatment' in i['text'].lower() or \
               'residual' in i['text'].lower() or 'review' in i['text'].lower() or \
               'threat' in i['text'].lower() or 'vulnerab' in i['text'].lower():
                print(f"  <{i['tag']}> '{i['text']}' pos=({i['x']},{i['y']}) href={i['href']}")

    browser.close()
