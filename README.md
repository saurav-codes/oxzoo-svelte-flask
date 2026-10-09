# oxzoo-svelte-flask: Flask API + Svelte SPA (ox deploy example)

Deployed with [ox](https://deploywithox.com): deploy a repo to your own server with one command, no Docker. [Docs](https://deploywithox.com/docs) · [Guide for this stack](https://deploywithox.com/docs/guides/flask)

This is the official ox documentation example for deploying a Flask 3 API (served by gunicorn from a uv-created venv, plain pip/requirements.txt flow) together with a Svelte 5 SPA built by Vite 5 onto one Ubuntu VPS. A single `ox.toml` at the repo root is the whole deploy contract: ox installs dependencies as the unprivileged project user, builds `dist/`, starts gunicorn on 127.0.0.1:9109 under systemd, and has nginx serve the SPA while proxying `/api` and `/health` to the app.

| Layer | Tool | Version |
|---|---|---|
| Backend framework | Flask | 3.1.3 |
| App server | gunicorn | 23.0.0 |
| Python env | uv (`uv venv` + `uv pip install -r requirements.txt`) | uv on the host |
| Frontend framework | Svelte | 5.57.0 |
| Bundler | Vite | 5.4.21 |
| Svelte plugin | @sveltejs/vite-plugin-svelte | 4.0.4 |
| Static hosting + proxy | nginx (`spa = true`) | managed by ox |
| Service supervision | systemd | managed by ox |

## Environment flow

- **Backend reads its env at RUNTIME.** `wsgi.py` builds the greeting from `os.environ["GREETING_TAG"]` on every request to `/api/greeting`; the value is never in the code. ox writes it to `/srv/ox/oxzoo-svelte-flask/env` from the dashboard Environment editor, so changing it only needs a service restart, not a rebuild.
- **Frontend reads its env at BUILD time.** `vite.config.js` sets `envPrefix: ["GREETING_", "VITE_"]`, so `GREETING_TAG` is exposed to the build and `import.meta.env.GREETING_TAG` is replaced by a string literal while bundling; `App.svelte` assembles the whole line in one expression that folds into a single bundle literal inside `dist/`. A new tag therefore needs a redeploy (rebuild), unlike the backend.
- **The pip flow (no pyproject).** The install hooks run as the unprivileged project user, so nothing installs globally: `uv venv .venv` creates the virtualenv inside the release, `uv pip install -r requirements.txt` installs the fully pinned lockfile, and `npm install` installs the exact-pinned frontend toolchain (package-lock.json is committed).
- **nginx** serves `dist/` with an `index.html` fallback (`spa = true`) and keeps only `/api` and `/health` proxied to the web process.

## Deploy with ox

1. Paste the clone URL into ox: `git@github.com:saurav-codes/oxzoo-svelte-flask`
2. Set `GREETING_TAG` in the Environment editor BEFORE the first deploy. The backend reads it at runtime and the frontend bakes it during the deploy build; without it the page shows the tag suffix empty.
3. Press Deploy and watch the live logs. ox runs the install and build hooks, starts gunicorn, and polls `http://127.0.0.1:9109/health` before switching traffic.

## Expected output

Opening the domain shows a heading and two labeled lines (here with a placeholder tag):

```
frontend: hello world oxzoo-svelte-flask_YOUR_TAG
backend: hello world oxzoo-svelte-flask_YOUR_TAG
```

`GET /health` returns 200 with body `ok`.
