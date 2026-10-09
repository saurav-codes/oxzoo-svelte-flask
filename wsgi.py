"""Flask app for the oxzoo-svelte-flask ox deploy example."""

import os

from flask import Flask

app = Flask(__name__)


@app.get("/api/greeting")
def greeting():
    # GREETING_TAG is an ox variable, read from the process env at runtime.
    return (
        f"hello world oxzoo-svelte-flask_{os.environ['GREETING_TAG']}",
        200,
        {"Content-Type": "text/plain; charset=utf-8"},
    )


@app.get("/health")
def health():
    return "ok", 200, {"Content-Type": "text/plain; charset=utf-8"}
