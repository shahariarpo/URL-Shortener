import secrets
import string

from urllib.parse import urlparse
from datetime import datetime, timezone

CODE_LENGTH = 6
ALPHABET = string.ascii_letters + string.digits


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def is_valid_url(value: str):
    value = value.strip()
    
    if not value or " " in value:
        return False
    try:
        parsed = urlparse(value)
    except ValueError:
        return False
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)

def generate_code(conn):
    while True:
        code = "".join(secrets.choice(ALPHABET) for _ in range(CODE_LENGTH))
        taken = conn.execute(
            "SELECT 1 FROM urls WHERE short_code = ?", (code,)
        ).fetchone()
        if taken is None:
            return code

if __name__ == "__main__":
    print(now_iso())
    for test in ["https://example.com", "http://a.com/x?y=1", "ftp://x.com", "http://", "not a url", "", "https://exa mple.com"]:
        print(f"{test!r:30} -> {is_valid_url(test)}")