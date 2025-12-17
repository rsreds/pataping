# ping-monitor

A minimal Flask web app that reads a list of hosts from `hosts.txt` and pings them, showing a simple web UI with green (up) / red (down) labels.

Features
- Backend: Flask endpoint `/api/status` that returns JSON with host statuses.
- Frontend: `static/index.html` shows status and auto-refreshes every 10s.
- Dockerfile for containerized runs.
- Example GitHub Actions deploy template and instructions for Render/Heroku.

Quick start (locally)

1. Create a virtualenv and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Edit `hosts.txt` with the hosts you want to monitor (one per line).

3. Run the app:

```bash
python app.py
```

Open http://localhost:8000

Docker

Build and run with Docker:

```bash
docker build -t ping-monitor:latest .
docker run -p 8000:8000 ping-monitor:latest
```

Notes on permissions and ping
- This app uses the system `ping` binary. On some systems `ping` requires elevated permissions or a setuid binary. The Debian/Ubuntu `iputils-ping` binary is typically available and will work inside the container.
- If you run into permission issues inside containers, ensure the `inetutils-ping` or `iputils-ping` package is present in the image.

Deploying from a Git repo

- Render: You can connect this GitHub repo to Render as a Web Service (choose Python, port 8000). Render will deploy on every push.
- Heroku: Add a Procfile `web: python app.py` and push to Heroku; set buildpacks for Python.
- Self-hosted via GitHub Actions: the included `.github/workflows/deploy.yml` is a template that demonstrates building and then SSHing to a server to run Docker pull/run. You must provide SSH-related secrets.

Testing

```bash
pip install -r requirements.txt
pip install pytest
pytest -q
```

License: MIT
