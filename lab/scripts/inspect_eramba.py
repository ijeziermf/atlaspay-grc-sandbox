"""
AtlasPay Sandbox — Eramba CE DOM inspector.

Instead of guessing Vue component selectors, this script lets Playwright load
each page, then dumps EVERY input/button/link element with its text, attributes,
and computed role. The output tells us exactly what to target.
"""
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path.home() / "Documents" / "IfeSec" / "Projects" / "atlaspay-grc-sandbox"
SHOTS = ROOT / "screenshots"
SHOTS.mkdir(parents=True, exist_ok=True)
OUT = ROOT / "docs" / "00-dom-inspection.txt"
OUT.parent.mkdir(parents=True, exist_ok=True)

ERAMBA_URL = "https://localhost:8443"
USER = "admin"
PASS = "8950Fourth"

def dump_dom(page, label: str):
    """Dump all interactive elements + their labels + key attributes."""
    print(f"\n=== {label} ===")
    # Use page.evaluate to extract structured data
    data = page.evaluate("""
        () => {
            const out = [];
            const sels = ['input', 'select', 'textarea', 'button', 'a[href]'];
            for (const sel of sels) {
                document.querySelectorAll(sel).forEach((el, idx) => {
                    const rect = el.getBoundingClientRect();
                    const visible = rect.width > 0 && rect.height > 0;
                    out.push({
                        tag: el.tagName.toLowerCase(),
                        type: el.getAttribute('type') || '',
                        name: el.getAttribute('name') || '',
                        id: el.id || '',
                        placeholder: el.getAttribute('placeholder') || '',
                        ariaLabel: el.getAttribute('aria-label') || '',
                        text: (el.innerText || el.value || '').trim().slice(0, 60),
                        href: el.getAttribute('href') || '',
                        classes: (el.className || '').toString().slice(0, 80),
                        visible: visible,
                        rect: { x: Math.round(rect.x), y: Math.round(rect.y),
                                w: Math.round(rect.width), h: Math.round(rect.height) },
                    });
                });
            }
            return out;
        }
    """)
    with OUT.open("a") as f:
        f.write(f"\n=== {label} ({time.strftime('%H:%M:%S')}) ===\n")
        for el in data:
            f.write(f"  <{el['tag']}{(' type=' + el['type']) if el['type'] else ''}"
                    f"{(' name=' + el['name']) if el['name'] else ''}"
                    f"{(' id=' + el['id']) if el['id'] else ''}"
                    f"{(' placeholder=' + repr(el['placeholder'])) if el['placeholder'] else ''}"
                    f"{(' aria-label=' + el['ariaLabel']) if el['ariaLabel'] else ''}>"
                    f" text={repr(el['text'])}"
                    f"{(' href=' + el['href']) if el['href'] else ''}"
                    f" visible={el['visible']}"
                    f"\n")
    print(f"  {len(data)} elements dumped to {OUT.name}")
    return data

# Start clean
OUT.write_text("Eramba CE DOM inspection\n==========================\n")

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--ignore-certificate-errors", "--no-sandbox"],
    )
    context = browser.new_context(
        ignore_https_errors=True,
        viewport={"width": 1440, "height": 900},
        locale="en-US",
        timezone_id="America/New_York",
    )
    page = context.new_page()

    # === Login page ===
    print("\n[1] Loading login page...")
    page.goto(ERAMBA_URL + "/login", wait_until="networkidle", timeout=60000)
    time.sleep(3)
    dump_dom(page, "LOGIN PAGE (before fill)")
    page.screenshot(path=str(SHOTS / "inspect-01-login.png"), full_page=True)

    # Try to log in by clicking the first 2 inputs in document order
    print("\n[2] Logging in by clicking first 2 inputs...")
    inputs = page.locator("input:visible").all()
    print(f"  Found {len(inputs)} visible inputs")
    if len(inputs) >= 2:
        inputs[0].fill(USER)
        inputs[1].fill(PASS)
        print(f"  Filled inputs[0]={USER}, inputs[1]=(password)")
    page.screenshot(path=str(SHOTS / "inspect-02-filled.png"), full_page=True)

    # Find and click "Sign in" — by text or button value
    buttons = page.locator("button:visible").all()
    print(f"  Found {len(buttons)} visible buttons")
    for btn in buttons:
        try:
            txt = btn.inner_text().strip()
            print(f"    button: {txt!r}")
            if 'sign' in txt.lower() or 'log' in txt.lower():
                print(f"    CLICKING: {txt!r}")
                btn.click()
                break
        except Exception:
            pass
    else:
        # Try submitting the form via Enter
        print("  No sign-in button found; pressing Enter on input[1]")
        inputs[1].press("Enter")

    page.wait_for_load_state("networkidle", timeout=30000)
    time.sleep(5)
    print(f"\n  URL after submit: {page.url}")
    page.screenshot(path=str(SHOTS / "inspect-03-after-login.png"), full_page=True)
    dump_dom(page, "AFTER LOGIN ATTEMPT")

    # === Dashboard ===
    if "/login" not in page.url:
        print("\n[3] Logged in. Capturing dashboard...")
        dump_dom(page, "DASHBOARD")
        page.screenshot(path=str(SHOTS / "inspect-04-dashboard.png"), full_page=True)

        # Try common sidebar links
        for label in ["Compliance", "Settings", "Organisations", "Frameworks"]:
            try:
                link = page.get_by_role("link", name=label, exact=False).first
                if link.is_visible(timeout=1000):
                    print(f"\n[4] Clicking sidebar link: {label}")
                    link.click()
                    page.wait_for_load_state("networkidle", timeout=15000)
                    time.sleep(2)
                    dump_dom(page, f"AFTER CLICK: {label}")
                    page.screenshot(path=str(SHOTS / f"inspect-05-{label.lower()}.png"),
                                    full_page=True)
            except Exception as e:
                print(f"  Could not click {label}: {e}")

    print("\nDone. Inspections saved to:")
    print(f"  {OUT}")
    print(f"  Screenshots: {SHOTS}")
    browser.close()
