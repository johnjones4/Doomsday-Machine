from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
import json
import os.path as path

def execute_google_contacts(logger, config, job):
    credentials = Credentials( 
        token=job["options"]["token"],
        refresh_token=job["options"]["refresh_token"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=job["options"]["client_id"],
        client_secret=job["options"]["client_secret"],
        scopes=["https://www.googleapis.com/auth/contacts.readonly"],
    )
    service = build("people", "v1", credentials=credentials)
    results = service.people().connections().list(
        resourceName='people/me',
        pageSize=2000,
        personFields='names,emailAddresses'
    ).execute()
    connections = results.get('connections', [])
    with open(path.join(job["output_folder"], "contacts.json"), "w") as contacts_file:
        logger.debug(f"Saving contacts")
        contacts_file.write(json.dumps(connections))
    
def generate_flow(job):
    return InstalledAppFlow.from_client_config({
        "installed": {
            "client_id": job["options"]["client_id"],
            "client_secret": job["options"]["client_secret"],
            "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        }
    }, ["https://www.googleapis.com/auth/contacts.readonly"], redirect_uri="urn:ietf:wg:oauth:2.0:oob")

def generate_login_url(job):
    flow = generate_flow(job)
    return flow.authorization_url()[0]

def authorize_code(job):
    flow = generate_flow(job)
    flow.fetch_token(code=job["options"]["code"])
    return {
        "token": flow.credentials.token,
        "refresh_token": flow.credentials.refresh_token
    }

