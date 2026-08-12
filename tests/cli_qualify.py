#!/usr/bin/env python3
"""Black-box qualification for the configuration-driven webhook CLI."""

from __future__ import annotations

from http.client import HTTPConnection
import os
from pathlib import Path
import socket
import subprocess
import time


ROOT = Path(__file__).resolve().parents[1]
TOKA = ROOT.parent / "toka"


def free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        probe.bind(("127.0.0.1", 0))
        return int(probe.getsockname()[1])


def request(port: int, secret: str, path: str = "/hooks/deploy", body: bytes = b"{}", trace: str | None = None, method: str = "POST", extra: dict[str, str] | None = None, content_type: str = "application/json") -> tuple[int, bytes, str | None]:
    connection = HTTPConnection("127.0.0.1", port, timeout=1)
    headers = {"X-Hook-Secret": secret}
    if trace is not None:
        headers["X-Trace"] = trace
    if extra is not None:
        headers.update(extra)
    headers["Content-Type"] = content_type
    connection.request(method, path, body=body, headers=headers)
    response = connection.getresponse()
    configured_header = response.getheader("X-Webhook-Response")
    body = response.read()
    connection.close()
    return response.status, body, configured_header


def main() -> int:
    toka = TOKA / "build" / "bin" / "toka"
    if not toka.is_file():
        raise RuntimeError("build ../toka before qualifying webhook")
    environment = os.environ | {"TOKA_LIB": str(TOKA / "lib")}
    subprocess.run([str(toka), "build"], cwd=ROOT, env=environment, check=True)

    port = free_port()
    server = subprocess.Popen(
        [str(ROOT / "target" / "debug" / "webhook"), "--hooks", str(ROOT / "tests" / "hooks.json"), "--port", str(port)],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    try:
        for _ in range(50):
            if server.poll() is not None:
                stdout, stderr = server.communicate()
                raise RuntimeError(f"webhook exited early: {stdout!r} {stderr!r}")
            try:
                status, body, configured_header = request(port, "correct-horse")
                break
            except OSError:
                time.sleep(0.02)
        else:
            raise RuntimeError("webhook did not accept a loopback connection")
        if (status, body) != (202, b"deployment accepted"):
            raise RuntimeError(f"authorized webhook response was {(status, body)!r}")
        if configured_header != "configured":
            raise RuntimeError(f"configured response header was {configured_header!r}")
        status, body, _ = request(port, "wrong")
        if status != 403 or body != b"hook trigger rule rejected request":
            raise RuntimeError(f"unauthorized webhook response was {(status, body)!r}")
        status, body, _ = request(port, "correct-horse", "/hooks/env")
        if status != 200 or body != b"webhook\n":
            raise RuntimeError(f"per-child environment response was {(status, body)!r}")
        status, body, _ = request(port, "correct-horse", "/hooks/query?message=hello+query")
        if status != 200 or body != b"hello query":
            raise RuntimeError(f"URL query command argument response was {(status, body)!r}")
        status, body, _ = request(port, "correct-horse", "/hooks/references", b"raw-body", "trace")
        if status != 200 or body != b"trace|raw-body|POST":
            raise RuntimeError(f"header/body/method command argument response was {(status, body)!r}")
        status, body, _ = request(port, "correct-horse", "/hooks/payload", b'{"repository":{"name":"toka"}}')
        if status != 200 or body != b"toka":
            raise RuntimeError(f"JSON payload command argument response was {(status, body)!r}")
        status, body, _ = request(port, "correct-horse", "/hooks/get-only", method="GET")
        if status != 200 or body != b"GET accepted":
            raise RuntimeError(f"configured GET method response was {(status, body)!r}")
        status, body, _ = request(port, "correct-horse", "/hooks/get-only")
        if status != 405 or body != b"":
            raise RuntimeError(f"disallowed method response was {(status, body)!r}")
        status, body, _ = request(port, "correct-horse", "/hooks/combined")
        if status != 200 or body != b"combined accepted":
            raise RuntimeError(f"nested trigger rule response was {(status, body)!r}")
        status, body, _ = request(port, "correct-horse", "/hooks/combined", extra={"X-Deny": "deny"})
        if status != 400 or body != b"hook trigger rule rejected request":
            raise RuntimeError(f"negated trigger rule response was {(status, body)!r}")
        status, body, _ = request(port, "", "/hooks/regex", extra={"X-Ref": "release-42"})
        if status != 200 or body != b"regex accepted":
            raise RuntimeError(f"regex trigger rule response was {(status, body)!r}")
        status, body, _ = request(port, "", "/hooks/regex", extra={"X-Ref": "main"})
        if status != 400 or body != b"hook trigger rule rejected request":
            raise RuntimeError(f"regex rejection response was {(status, body)!r}")
        status, body, _ = request(port, "correct-horse", "/hooks/headers")
        if status != 200 or b'"x-hook-secret":"correct-horse"' not in body:
            raise RuntimeError(f"complete header response was {(status, body)!r}")
        status, body, _ = request(port, "correct-horse", "/hooks/form", b"message=hello+form", content_type="application/x-www-form-urlencoded")
        if status != 200 or body != b"hello form":
            raise RuntimeError(f"form payload response was {(status, body)!r}")
        status, body, _ = request(port, "correct-horse", "/hooks/xml", b"<repository><name>toka-xml</name></repository>", content_type="application/xml")
        if status != 200 or body != b"toka-xml":
            raise RuntimeError(f"XML payload response was {(status, body)!r}")
    finally:
        server.terminate()
        try:
            server.wait(timeout=3)
        except subprocess.TimeoutExpired:
            server.kill()
            server.wait(timeout=3)
    print("toka-webhook CLI qualification: PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
