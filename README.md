# PATAPING

A minimal Flask web app that reads a list of hosts from `hosts.txt` and pings them, showing a simple web UI with green (up) / red (down) labels.

Features
- Backend: Flask endpoint `/api/status` that returns JSON with host statuses.
- Frontend: `static/index.html` shows status and auto-refreshes every 30s.
- Dockerfile for containerized runs.

## Quick start (local)

1. Create a virtualenv and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Edit `hosts.txt` with the hosts you want to monitor (one per line). You may optionally provide a name before the host/IP, e.g.:

```
localhost 127.0.0.1
8.8.8.8
```

If a name is provided, the UI shows the name in bold and the host next to it; otherwise the host is shown in bold.

3. Run the app:

```bash
python app.py
```

Open http://localhost:8000

## Docker

Build and run with Docker:

```bash
docker build -t pataping:latest .
docker run -p 8000:8000 pataping:latest
```

## CERN PaaS Deployment

The app can be deployed to CERN PaaS using the provided `Dockerfile`. Make sure to set up the `hosts.txt` file appropriately before building the image. Follow [CERN PaaS documentation](https://paas.docs.cern.ch/) for deployment steps.

> [!NOTE]
> **Notes on permissions and ping**
> - This app uses the system `ping` binary. On some systems `ping` requires elevated permissions or a setuid binary. The Debian/Ubuntu `iputils-ping` binary is typically available and will work inside the container.
> - If you run into permission issues inside containers, ensure the `inetutils-ping` or `iputils-ping` package is present in the image.