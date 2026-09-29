from slowapi import Limiter
from fastapi import Request

def get_client_ip(request: Request) -> str:
    return request.headers.get(
        "x-real-ip",
        request.headers.get("x-forwarded-for", "").split(",")[0].strip()
        or request.client.host,
    )

limiter = Limiter(key_func=get_client_ip)