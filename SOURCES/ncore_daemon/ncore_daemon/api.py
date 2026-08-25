from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, PlainTextResponse

from ncore_daemon.amp import Amp
from ncore_daemon.sources import SOURCE_LIST


def get_amp(app: FastAPI) -> Amp:
    return app.state.amp


DEBUG_HTML = """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8"/>
  <title>Ncore / aurora</title>
  <style>
    body { font-family: sans-serif; margin: 2rem; line-height: 1.6; }
    a { margin-right: 0.5rem; }
  </style>
</head>
<body>
  <h1>Ncore / aurora</h1>
  <p>
    <a href="#" data-url="/state/on">on</a> /
    <a href="#" data-url="/state/off">off</a>
  </p>
  <p>
    <a href="#" data-url="/volume/down">vol down</a> /
    <a href="#" data-url="/volume/up">vol up</a>
  </p>
  <p id="sources"></p>
  <pre id="status"></pre>
  <script>
    const sources = ["usb","optical_1","optical_2","optical_3","optical_4","analog_1","analog_2","analog_3","analog_4"];
    const box = document.getElementById("sources");
    sources.forEach(s => {
      const a = document.createElement("a");
      a.href = "#";
      a.dataset.url = "/input/" + s;
      a.textContent = s;
      box.appendChild(a);
      box.appendChild(document.createElement("br"));
    });
    async function refresh() {
      const r = await fetch("/status");
      document.getElementById("status").textContent = JSON.stringify(await r.json(), null, 2);
    }
    document.body.addEventListener("click", async (e) => {
      const a = e.target.closest("a[data-url]");
      if (!a) return;
      e.preventDefault();
      await fetch(a.dataset.url, { method: "PUT" });
      await refresh();
    });
    refresh();
  </script>
</body>
</html>
"""


def install_routes(app: FastAPI) -> None:
    @app.get("/", response_class=HTMLResponse)
    async def root():
        return DEBUG_HTML

    @app.get("/status")
    async def status():
        return get_amp(app).status()

    @app.get("/state")
    async def get_state():
        return get_amp(app).state

    @app.put("/state/{state}")
    async def put_state(state: str):
        if state not in ("on", "off"):
            raise HTTPException(400, "state must be on or off")
        amp = get_amp(app)
        if state == "on":
            ok = await amp.power_on()
            if not ok:
                raise HTTPException(503, "DSP or GPIO failed; amp not enabled")
        else:
            await amp.power_off()
        return amp.status()

    @app.get("/volume")
    async def get_volume():
        return get_amp(app).volume

    @app.put("/volume/{vol}")
    async def put_volume(vol: str):
        amp = get_amp(app)
        if vol == "up":
            await amp.volume_up()
        elif vol == "down":
            await amp.volume_down()
        else:
            if not vol.isdigit():
                raise HTTPException(400, "volume must be up, down, or an integer")
            await amp.set_volume(int(vol))
        return amp.status()

    @app.get("/input")
    async def get_input():
        return get_amp(app).source

    @app.put("/input/{source}")
    async def put_input(source: str):
        if source not in SOURCE_LIST:
            raise HTTPException(400, f"unknown source: {source}")
        amp = get_amp(app)
        await amp.set_source(source)
        return amp.status()

    @app.get("/resetdsp", response_class=PlainTextResponse)
    async def reset_dsp():
        await get_amp(app).reset_dsp()
        return "OK"
