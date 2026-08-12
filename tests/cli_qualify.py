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


def request(port: int, secret: str) -> tuple[int, bytes]:
    connection = HTTPConnection("127.0.0.1", port, timeout=1)
    connection.request("POST", "/hooks/deploy", body=b"{}", headers={"X-Hook-Secret": secret})
    response = connection.getresponse()
    body = response.read()
    connection.close()
    return response.status, body


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
                status, body = request(port, "correct-horse")
                break
            except OSError:
                time.sleep(0.02)
        else:
            raise RuntimeError("webhook did not accept a loopback connection")
        if (status, body) != (200, b"hook triggered"):
            raise RuntimeError(f"authorized webhook response was {(status, body)!r}")
        status, body = request(port, "wrong")
        if status != 400 or body != b"hook trigger rule rejected request":
            raise RuntimeError(f"unauthorized webhook response was {(status, body)!r}")
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
