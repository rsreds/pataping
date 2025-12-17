from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import partial
from pathlib import Path
import subprocess
import json
from datetime import datetime, timezone

from flask import Flask, jsonify, send_from_directory

BASE_DIR = Path(__file__).parent
HOSTS_FILE = BASE_DIR / "hosts.txt"

app = Flask(__name__, static_folder="static", static_url_path="")


def ping_host(host: str, timeout_sec: int = 1) -> dict:
    """Ping a host once using system ping. Returns dict with status and latency_ms."""
    host = host.strip()
    if not host:
        return {"host": host, "status": "invalid", "latency_ms": None}

    cmd = ["ping", "-c", "1", "-W", str(timeout_sec), host]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if res.returncode == 0:
            # try to parse latency
            out = res.stdout
            latency = None
            # look for 'time=X ms'
            for part in out.split():
                if part.startswith("time="):
                    try:
                        latency = float(part.split("=")[1])
                    except Exception:
                        latency = None
                        break
            return {"host": host, "status": "up", "latency_ms": latency}
        else:
            return {"host": host, "status": "down", "latency_ms": None}
    except FileNotFoundError:
        # ping binary not found
        return {"host": host, "status": "error", "latency_ms": None, "error": "ping binary not found"}


@app.route("/api/status")
def api_status():
    """Return JSON status for each host listed in hosts.txt"""
    if not HOSTS_FILE.exists():
        return jsonify({"error": "hosts file not found", "path": str(HOSTS_FILE)}), 500

    # parse lines that may be either:
    # - host
    # - name host
    raw_lines = [line.strip() for line in HOSTS_FILE.read_text().splitlines() if line.strip() and not line.strip().startswith("#")]

    entries = []
    for ln in raw_lines:
        parts = ln.split()
        if len(parts) >= 2:
            name = parts[0]
            host = parts[1]
        else:
            name = None
            host = parts[0]
        entries.append((name, host))

    results = []
    # use timezone-aware UTC datetime to avoid DeprecationWarning
    now = datetime.now(timezone.utc).isoformat()

    # Submit futures in the original order and collect results in the same order
    with ThreadPoolExecutor(max_workers=20) as ex:
        futures = [ex.submit(ping_host, host) for (name, host) in entries]
        for i, fut in enumerate(futures):
            name, host = entries[i]
            try:
                item = fut.result()
                # attach name if present
                if name:
                    item["name"] = name
                else:
                    item.setdefault("name", None)
                results.append(item)
            except Exception as e:
                results.append({"host": host, "name": name, "status": "error", "latency_ms": None, "error": str(e)})

    return jsonify({"checked_at": now, "results": results})


@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
