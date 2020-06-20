from flask import Flask, jsonify, send_from_directory
from doomsdaymachine.util import load_config
from doomsdaymachine.backup_log import BackupLog

APP = Flask(__name__)

config = load_config()

ALLOWED_STATIC_FILES = [
    "index.html",
    "script.js",
    "style.css",
    "reset.css",
]

@APP.route("/")
def home_file():
    return send_from_directory("../static", "index.html")

@APP.route("/<file>")
def static_file(file):
    if file in ALLOWED_STATIC_FILES:
        return send_from_directory("../static", file)

@APP.route("/api/status")
def status():
    backup_log = BackupLog(config)
    active_job = backup_log.get_active_job()
    jobs = list(map(lambda job: dict(
        name=job["name"],
        type=job["type"],
        id=job["id"],
        start_time=active_job["start_time"] if active_job["job"] == job["id"] else None,
        last_execution_time=backup_log.get_last_execution_time(job["id"])
    ), config["jobs"]))
    return jsonify(dict(jobs=jobs))
