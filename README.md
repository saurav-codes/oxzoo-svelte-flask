# oxzoo-svelte-flask: Flask API + Svelte SPA (ox deploy example)

Deployed with [ox](https://deploywithox.com): deploy a repo to your own server with one command, no Docker. [Docs](https://deploywithox.com/docs) · [Guide for this stack](https://deploywithox.com/docs/guides/flask)

An [ox](https://deploywithox.com) deploy example: a Flask 3.1 API on gunicorn, installed from a pinned `requirements.txt`, with a Svelte 5 SPA built by Vite, deployed to your own Ubuntu server. systemd runs gunicorn, and Caddy serves the built SPA with an `index.html` fallback while sending only `/api` and `/health` to Flask.

## Stack

| Layer | Tool | Role |
|---|---|---|
| Frontend | Svelte 5 + Vite 5 | SPA built to `dist/` from `client/` |
| API | Flask 3.1 on gunicorn 23 | `GET /api/greeting` and `GET /health` |
| Python | 3.13 with uv | `requirements.txt` pins every package |
| Node | 24 | `package-lock.json` is committed |

## ox.toml

```toml
# Flask API on gunicorn (pip requirements) + Svelte SPA (npm) in one repo.

[app]
start  = ".venv/bin/gunicorn wsgi:app --bind 127.0.0.1:$PORT --workers 2"
health = "/health"

[static]
dir = "dist"
spa = true
api = ["/api", "/health"]

[build]
commands = ["uv venv .venv && uv pip install --python .venv -r requirements.txt", "npm run build"]

[tools]
python = "3.13"
uv     = "0.11"
node   = "24"
```

The repo has two languages, so `[build] commands` names both: `npm ci` is detected from `package-lock.json` and runs first, then the venv and the SPA build. In a Python-only repo ox would detect the `requirements.txt` install by itself.

## Environment flow

- **Run time (API):** `wsgi.py` reads `GREETING_TAG` on every `GET /api/greeting`.
- **Build time (SPA):** `vite.config.js` sets `envPrefix: ["GREETING_", "VITE_"]`, so the Svelte app reads `import.meta.env.GREETING_TAG` and Vite bakes it into `dist/`. ox sets your variables before the build, and changing one with `ox vars set` redeploys, which rebuilds the SPA.

## Deploy with ox

```sh
curl -fsSL https://deploywithox.com/install.sh | sh
ox login
ox new https://github.com/saurav-codes/oxzoo-svelte-flask
printf 'GREETING_TAG=demo\n' | ox review oxzoo-svelte-flask --from-file - --wait
```

The plan, offline:

```console
$ ox check .
ox check . (manifest: ox.toml)

  app.start                  .venv/bin/gunicorn wsgi:app --bind 127.0.0.1:$PORT --workers 2 declared
  app.health                 /health                                              declared
  static.dir                 dist                                                 declared
  static.spa                 true                                                 declared
  static.api                 /api, /health                                        declared
  build.install              npm ci                                               detected:package-lock.json
  build.commands[0]          uv venv .venv && uv pip install --python .venv -r requirements.txt declared
  build.commands[1]          npm run build                                        declared
  tools.node                 24                                                   declared
  tools.python               3.13                                                 declared
  tools.uv                   0.11                                                 declared

  Provided by ox: PORT, HOST, OX_ENV, OX_PROJECT, OX_RELEASE, OX_DATA_DIR, PUBLIC_URL, PUBLIC_HOST
  Set on the dashboard before the first deploy: GREETING_TAG

Ready to deploy.
```

## Expected output

```
frontend: hello world oxzoo-svelte-flask_<GREETING_TAG>
backend: hello world oxzoo-svelte-flask_<GREETING_TAG>
```

## Local development

```sh
npm ci && GREETING_TAG=dev npm run build
uv venv .venv && uv pip install --python .venv -r requirements.txt
GREETING_TAG=dev .venv/bin/gunicorn wsgi:app --bind 127.0.0.1:9109
```
