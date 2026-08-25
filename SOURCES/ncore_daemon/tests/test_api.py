from fastapi.testclient import TestClient

from ncore_daemon.app import create_app
from ncore_daemon.config import Settings
from tests.conftest import make_amp


def test_status_and_aliases(tmp_path):
    amp = make_amp()
    settings = Settings(dry_run=True, state_path=str(tmp_path / "state.json"))
    app = create_app(settings, amp=amp, enable_ir=False)
    with TestClient(app) as client:
        status = client.get("/status").json()
        assert status["state"] == "off"
        assert status["serial_ok"] is True
        assert status["gpio_ok"] is True
        assert "usb" in status["source_list"]
        assert client.get("/state").json() == "off"
        on = client.put("/state/on")
        assert on.status_code == 200
        assert on.json()["state"] == "on"
        vol = client.put("/volume/15")
        assert vol.status_code == 200
        src = client.put("/input/analog_2")
        assert src.json()["source"] == "analog_2"
        assert client.get("/resetdsp").text == "OK"


def test_unknown_source_rejected(tmp_path):
    amp = make_amp()
    settings = Settings(dry_run=True, state_path=str(tmp_path / "state.json"))
    app = create_app(settings, amp=amp, enable_ir=False)
    with TestClient(app) as client:
        response = client.put("/input/hdmi")
        assert response.status_code == 400
