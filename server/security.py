"""Zabezpečení místního serveru: token, kontrola hlaviček Host a Origin.

Server spouští kód, takže cizí web v prohlížeči nesmí umět poslat požadavek na /api/run.
- Host musí být 127.0.0.1 nebo localhost s naším portem (ochrana proti DNS rebindingu).
- Origin, pokud je přítomen, musí být náš vlastní.
- Požadavky měnící stav nebo spouštějící kód musí nést náhodný token.
"""
import hmac
import secrets
from urllib.parse import urlsplit

ALLOWED_HOSTS = ("127.0.0.1", "localhost")


def new_token() -> str:
    return secrets.token_urlsafe(24)


def host_ok(host_header: str | None, port: int) -> bool:
    if not host_header:
        return False
    return host_header.lower() in {f"{h}:{port}" for h in ALLOWED_HOSTS}


def origin_ok(origin_header: str | None, port: int) -> bool:
    """Chybějící Origin je v pořádku (stejný původ u GET), jinak musí být náš."""
    if origin_header is None:
        return True
    try:
        u = urlsplit(origin_header)
    except ValueError:
        return False
    return u.scheme == "http" and u.hostname in ALLOWED_HOSTS and u.port == port


def token_ok(sent: str | None, expected: str) -> bool:
    return bool(sent) and hmac.compare_digest(sent, expected)
