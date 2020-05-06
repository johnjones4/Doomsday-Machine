import lastpass
import json
import os.path as path

def execute_lastpass(logger, config, job):
    vault = lastpass.Vault.open_remote(job["options"]["username"], job["options"]["password"])
    output = []
    for account in vault.accounts:
        logger.debug(f"Saving account {account.id.decode('utf-8')}")
        output.append({
            "id": account.id.decode("utf-8"),
            "username": account.username.decode("utf-8"),
            "password": account.password.decode("utf-8"),
            "url": account.url.decode("utf-8")
        })
    with open(path.join(job["output_folder"], "passwords.json"), "w") as passwords_file:
        logger.debug(f"Saving accounts")
        passwords_file.write(json.dumps(output))
