"""Click the Settings dropdown caret to find Calculation Method + Risk Appetite forms."""
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
    page.screenshot(path=str(SHOTS / "600-risks-page.png"), full_page=True)

    # Click the dropdown caret NEXT to Settings (it's a separate button)
    # From the earlier dump, it's button[aria-label='Settings'] + a sibling
    print("Looking for buttons near the Settings button...")
    btns = page.evaluate("""
        () => {
            const settings_btn = document.querySelector('button[aria-label="Settings"]');
            if (!settings_btn) return [];
            // Find sibling/parent buttons
            const parent = settings_btn.parentElement;
            const all = parent.querySelectorAll('button, a');
            return Array.from(all).map(el => ({
                tag: el.tagName.toLowerCase(),
                text: (el.innerText || el.value || '').trim().slice(0, 60),
                cls: (el.className || '').toString().slice(0, 100),
                ariaLabel: el.getAttribute('aria-label') || '',
                visible: el.getBoundingClientRect().width > 0
            }));
        }
    """)
    for b in btns:
        print(f"  <{b['tag']}> '{b['text']}' aria={b['ariaLabel']} cls={b['cls'][:60]}")

    # Click the caret (the i.ri-arrow-down-s-line or similar)
    print("\nLooking for caret icon next to Settings...")
    caret = page.locator("button[aria-label='Settings'] + button, button[aria-label='Settings'] ~ button").first
    if caret.count() > 0:
        try:
            caret.click(timeout=3000)
            time.sleep(2)
            page.screenshot(path=str(SHOTS / "601-settings-caret-open.png"), full_page=True)

            items = page.evaluate("""
                () => Array.from(document.querySelectorAll('.dropdown-menu a, [role="menu"] a')).filter(el => el.getBoundingClientRect().width > 0).map(el => ({
                    text: (el.innerText || '').trim().slice(0, 60),
                    href: el.getAttribute('href') || ''
                }))
            """)
            print(f"  Dropdown items: {len(items)}")
            for i in items[:20]:
                print(f"    '{i['text']}' -> {i['href']}")
        except Exception as e:
            print(f"  caret click: {e}")

    # Also click the + button in the toolbar
    print("\nClicking the '+' button in toolbar (after Views)...")
    plus = page.locator("button:has-text('+')").first
    if plus.is_visible(timeout=3000):
        plus.click()
        time.sleep(2)
        page.screenshot(path=str(SHOTS / "602-plus-button-clicked.png"), full_page=True)
        items = page.evaluate("""
            () => Array.from(document.querySelectorAll('.dropdown-menu a, [role="menu"] a')).filter(el => el.getBoundingClientRect().width > 0).map(el => ({
                text: (el.innerText || '').trim().slice(0, 60),
                href: el.getAttribute('href') || ''
            }))
        """)
        print(f"  + button dropdown items: {len(items)}")
        for i in items[:20]:
            print(f"    '{i['text']}' -> {i['href']}")

    # Try clicking the secondary dropdown caret to the right of Settings
    print("\nTrying second button next to Settings...")
    second = page.locator("button.shrink-0, button:has(i.ri-arrow-down-s-line)").first
    if second.count() > 0 and second.is_visible(timeout=2000):
        try:
            second.click()
            time.sleep(2)
            page.screenshot(path=str(SHOTS / "603-secondary-caret.png"), full_page=True)
            items = page.evaluate("""
                () => Array.from(document.querySelectorAll('.dropdown-menu a')).filter(el => el.getBoundingClientRect().width > 0).map(el => ({
                    text: (el.innerText || '').trim().slice(0, 60)
                }))
            """)
            print(f"  secondary dropdown: {len(items)} items")
            for i in items[:20]:
                print(f"    '{i['text']}'")
        except Exception as e:
            print(f"  secondary click: {e}")

    browser.close()
