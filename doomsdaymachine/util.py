import hashlib
import yaml
import os.path as path
import string 

def load_config():
    with open("/var/lib/doomsday/config.yml", "r") as config_file:
        config = yaml.full_load(config_file)
        if "jobs" not in config:
            raise Exception(f"No config jobs provided")
        id_map = {}
        for i, job in enumerate(config["jobs"]):
            if "name" not in job:
                raise Exception(f"No name provided for job #{i}")
            if "type" not in job:
                raise Exception(f"No type provided for job #{i}")
            job_id = generate_job_id(job)
            if job_id in id_map and id_map[job_id] != i:
                raise Exception(f"Job name and type must be unique (Error on job #{i})")
            else:
                id_map[job_id] = i
                job["id"] = job_id
        return config


def generate_job_id(job):
    return hashlib.sha256(f"{job['name']}-{job['type']}".encode()).hexdigest()


def format_filename(s):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in s if c in valid_chars)
    filename = filename.replace(' ','_') # I don't like spaces in filenames.
    return filename
