from doomsdaymachine.datasources import google_drive, google_contacts
from doomsdaymachine.util import load_config
import sys

def generate(name):
    config = load_config()
    for job in config["jobs"]:
        if job["name"] == name:
            if job["type"] == "google_contacts":
                if "code" in job["options"]:
                    print(google_contacts.authorize_code(job))
                else:
                    print(google_contacts.generate_login_url(job))
            elif job["type"] == "google_drive":
                if "code" in job["options"]:
                    print(google_drive.authorize_code(job))
                else:
                    print(google_drive.generate_login_url(job))

generate(sys.argv[1])
