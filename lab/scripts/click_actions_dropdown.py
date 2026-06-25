"""Click the 'Actions' dropdown on /risks/classifications to find Add."""
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

    page.goto(ERAMBA_URL + "/risks/classifications", wait_until="networkidle", timeout=30000)
    time.sleep(3)
    page.screenshot(path=str(SHOTS / "320-classifications-with-actions.png"), full_page=True)

    # Click the Actions dropdown
    print("Clicking 'Actions'...")
    actions = page.locator("a.dropdown-toggle:has-text('Actions')").first
    if actions.is_visible(timeout=3000):
        actions.click()
        time.sleep(2)
        page.screenshot(path=str(SHOTS / "321-actions-open.png"), full_page=True)

        # Find menu items in the dropdown
        items = page.evaluate("""
            () => Array.from(document.querySelectorAll('.dropdown-menu a, .dropdown-menu li, [role="menu"] a, [role="menuitem"]')).map(el => ({
                tag: el.tagName.toLowerCase(),
                text: (el.innerText || '').trim().slice(0, 60),
                href: el.getAttribute('href') || '',
                visible: el.getBoundingClientRect().width > 0
            })).filter(el => el.visible)
        """)
        print(f"Dropdown items: {len(items)}")
        for i in items[:15]:
            print(f"  <{i['tag']}> '{i['text']}' -> {i['href']}")

        # Click the "Add" item
        try:
            add_item = page.locator(".dropdown-menu a:has-text('Add')").first
            if add_item.is_visible(timeout=3000):
                add_item.click()
                time.sleep(2)
                page.screenshot(path=str(SHOTS / "322-add-form.png"), full_page=True)
                # Find inputs
                inputs = page.evaluate("""
                    () => Array.from(document.querySelectorAll('input, select, textarea')).filter(el => el.getBoundingClientRect().width > 0).map(el => ({
                        tag: el.tagName.toLowerCase(),
                        type: el.type || '',
                        name: el.name || '',
                        id: el.id || '',
                        placeholder: el.placeholder || '',
                        value: el.value || ''
                    }))
                """)
                print(f"\nForm inputs ({len(inputs)}):")
                for i in inputs:
                    print(f"  <{i['tag']}> type={i['type']} name={i['name']} id={i['id']} placeholder={i['placeholder']}")
        except Exception as e:
            print(f"ERROR clicking Add: {e}")
    else:
        print("Actions dropdown not visible")

    browser.close()
