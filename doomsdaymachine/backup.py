import time
import os
import os.path as path
import logging
from doomsdaymachine.datasources.dropbox import execute_dropbox
from doomsdaymachine.datasources.google_contacts import execute_google_contacts
from doomsdaymachine.datasources.lastpass import execute_lastpass
from doomsdaymachine.datasources.github import execute_github
from doomsdaymachine.datasources.imap import execute_imap
from doomsdaymachine.datasources.google_drive import execute_google_drive
from doomsdaymachine.util import load_config
from doomsdaymachine.notification import send_notification
from doomsdaymachine.backup_log import BackupLog

def start():
    config = load_config()
    logger = logging.getLogger(__name__)
    handler = logging.FileHandler(config["log"]["file"]) if "log" in config and "file" in config["log"] else logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.getLevelName(config["log"]["level"]) if "log" in config and "level" in config["log"] else logging.INFO)
    i = 0
    backup_log = BackupLog(config)
    while True:
        config["output"] = config["outputs"][i]
        i = i + 1 if i + 1 < len(config["outputs"]) else 0
        for job in config["jobs"]:
            job["output_folder"] = path.join(config["output"], job["id"])
            try:
                (start_time, job_instance_id) = backup_log.start_job(job["id"])
                execute_job(logger, config, job)
                end_time = backup_log.end_job(job["id"], job_instance_id)
                elapsed_time = time.time() - end_time
                send_notification(config, f"Completed {job['type']}/{job['name']} to {job['output_folder']} in {elapsed_time} seconds.")
            except Exception as e:
                logger.error(f"Exception during {job['type']}/{job['name']} to {job['output_folder']}", exc_info=True)
                send_notification(config, f"Exception during {job['type']}/{job['name']} to {job['output_folder']}: {str(e)}.")
            if "delay" in config and "job" in config["delay"]:
                time.sleep(config["delay"]["job"])
        if "delay" in config and "cycle" in config["delay"]:
            time.sleep(config["delay"]["cycle"])


def execute_job(logger, config, job):
    logger.info(f"Starting {job['type']}/{job['name']} ({job['id']})")
    if not path.isdir(job["output_folder"]):
        os.mkdir(job["output_folder"])
    if job["type"] == "dropbox":
        execute_dropbox(logger, config, job)
    elif job["type"] == "google_contacts":
        execute_google_contacts(logger, config, job)
    elif job["type"] == "lastpass":
        execute_lastpass(logger, config, job)
    elif job["type"] == "github":
        execute_github(logger, config, job)
    elif job["type"] == "imap":
        execute_imap(logger, config, job)
    elif job["type"] == "google_drive":
        execute_google_drive(logger, config, job)
