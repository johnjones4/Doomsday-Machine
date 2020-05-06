from doomsdaymachine.datasources.google_contacts import generate_login_url, authorize_code
from doomsdaymachine.util import load_config


def generate():
    config = load_config()
    for job in config["jobs"]:
        if job["type"] == "google_contacts":
            if "code" in job["options"]:
                print(authorize_code(job))
            else:
                print(generate_login_url(job))

generate()
