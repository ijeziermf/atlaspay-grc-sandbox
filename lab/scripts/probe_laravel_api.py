"""Probe the /laravel/api/ endpoints directly to understand the API contract."""
import json
import urllib.request
import urllib.error
import ssl
from http.cookiejar import CookieJar

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Login to get session cookie + CSRF
cj = CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj), urllib.request.HTTPSHandler(context=ctx))

ERAMBA_URL = "https://localhost:8443"

# Get login page to obtain CSRF cookie
req = urllib.request.Request(f"{ERAMBA_URL}/login", headers={'User-Agent': 'Mozilla/5.0'})
resp = opener.open(req, timeout=15)
body = resp.read().decode('utf-8', errors='ignore')
print(f"GET /login: {resp.status}")

# Submit login
import re
m = re.search(r'name="_csrfToken"[^>]*value="([^"]+)"', body)
csrf_token_input = m.group(1) if m else ''
m2 = re.search(r'csrfToken=([^"&;]+)', body)
csrf_token_cookie = m2.group(1) if m2 else ''
print(f"  CSRF input: {csrf_token_input[:30]}...")
print(f"  CSRF cookie: {csrf_token_cookie[:30]}...")

# Login POST
data = urllib.parse.urlencode({
    '_method': 'POST',
    'data[User][login]': 'admin',
    'data[User][password]': '8950Fourth',
    '_csrfToken': csrf_token_input,
}).encode()

req = urllib.request.Request(
    f"{ERAMBA_URL}/users/login",
    data=data,
    headers={
        'User-Agent': 'Mozilla/5.0',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRF-Token': csrf_token_cookie,
        'Referer': f"{ERAMBA_URL}/login",
    },
    method='POST',
)
try:
    resp = opener.open(req, timeout=15)
    print(f"POST /users/login: {resp.status}")
    print(f"  body: {resp.read()[:300]}")
except urllib.error.HTTPError as e:
    print(f"  HTTP {e.code}: {e.read()[:300]}")

# Now try API endpoints
print("\n=== API probes ===")
for path in [
    "/laravel/api/risks",
    "/laravel/api/security-policies",
    "/laravel/api/business-continuity-plans",
    "/laravel/api/third-parties",
    "/laravel/api/security-incidents",
    "/laravel/api/risk-classifications",
    "/laravel/api/risk-classification-types",
    "/laravel/api/users/login",
]:
    try:
        req = urllib.request.Request(
            f"{ERAMBA_URL}{path}",
            headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json'}
        )
        resp = opener.open(req, timeout=10)
        body = resp.read().decode('utf-8', errors='ignore')
        print(f"  GET {path}: {resp.status} {len(body)} bytes")
        if len(body) < 1000:
            print(f"    body: {body[:300]}")
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', errors='ignore')
        print(f"  GET {path}: HTTP {e.code} {body[:200]}")
    except Exception as e:
        print(f"  GET {path}: ERROR {e}")
