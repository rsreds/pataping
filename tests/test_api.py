import tempfile
from pathlib import Path

import pytest

from app import app, HOSTS_FILE


def test_api_status_empty_hosts(monkeypatch, tmp_path):
    # create a temporary hosts file with a known host
    tmp_hosts = tmp_path / "hosts.txt"
    tmp_hosts.write_text("127.0.0.1\n")

    monkeypatch.setattr('app.HOSTS_FILE', tmp_hosts)

    client = app.test_client()
    res = client.get('/api/status')
    assert res.status_code == 200
    data = res.get_json()
    assert 'results' in data
    assert isinstance(data['results'], list)
