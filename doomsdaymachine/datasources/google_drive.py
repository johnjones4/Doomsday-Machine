from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.urllib3 import Request
import json
import os.path as path
import urllib3
import os
from doomsdaymachine.sync_map import SyncMap
import io
import datetime

EXPORTABLE = {
    "application/vnd.google-apps.spreadsheet": "application/x-vnd.oasis.opendocument.spreadsheet",
    "application/vnd.google-apps.presentation": "application/vnd.oasis.opendocument.presentation",
    "application/vnd.google-apps.document": "application/vnd.oasis.opendocument.text",
    "application/vnd.google-apps.drawing": "image/svg+xml"
}

IGNORE = [
    "application/vnd.google-apps.folder",
    "application/vnd.google-apps.form",
    "application/vnd.google-apps.fusiontable",
    "application/vnd.google-apps.map",
    "application/vnd.google-apps.script",
    "application/vnd.google-apps.shortcut",
    "application/vnd.google-apps.site",
    "application/vnd.google-apps.unknown"
]

EXTENSIONS = {
    "application/vnd.google-apps.spreadsheet": "ods",
    "application/vnd.google-apps.presentation": "odp",
    "application/vnd.google-apps.document": "odt",
    "application/vnd.google-apps.drawing": "svg"
}

def execute_google_drive(logger, config, job):
    credentials = Credentials( 
        token=job["options"]["token"],
        refresh_token=job["options"]["refresh_token"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=job["options"]["client_id"],
        client_secret=job["options"]["client_secret"],
        scopes=[ "https://www.googleapis.com/auth/drive.readonly"],
    )
    credentials.refresh(Request(urllib3.PoolManager()))
    service = build('drive', 'v3', credentials=credentials)

    syncer = SyncMap(job)

    file_output_folder = path.join(job["output_folder"], "files")
    if not path.isdir(file_output_folder):
        os.mkdir(file_output_folder)

    results = None
    pageToken = None
    while not results or pageToken:
        results = service.files().list(
            pageSize=100,
            fields="nextPageToken, files(*)",
            pageToken=pageToken
        ).execute()
        pageToken = results.get('nextPageToken', None)
        for item in results.get('files', []):
            try:
                modified_time = datetime.datetime.strptime(item["modifiedTime"], "%Y-%m-%dT%H:%M:%S.%fZ").timestamp()
                if modified_time > syncer.get_last_modified(item["id"]) and item["capabilities"]["canDownload"] and item["mimeType"] not in IGNORE:
                    if item["mimeType"] in EXPORTABLE:
                        request = service.files().export(
                            fileId=item["id"],
                            mimeType=EXPORTABLE[item["mimeType"]]
                        )
                        output_file = item["id"] + "_" + item["name"].strip().replace("/", "-") + "." + EXTENSIONS[item["mimeType"]]
                    else:
                        request = service.files().get_media(fileId=item["id"])
                        output_file = item["id"] + "_" + item["name"].strip().replace("/", "-")
                    if request:
                        logger.debug(f"Downloading: {item['name']}")
                        with open(path.join(file_output_folder, output_file), "wb") as output_file_handler:
                            downloader = MediaIoBaseDownload(output_file_handler, request)
                            done = False
                            while not done:
                                _, done = downloader.next_chunk()
                    syncer.set_last_modified(item["id"], modified_time)
            except:
                logger.error(f"Exception during {job['type']}/{job['name']} to {job['output_folder']}", exc_info=True)
        syncer.save()
    syncer.close()


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
    }, ["https://www.googleapis.com/auth/drive.readonly"], redirect_uri="urn:ietf:wg:oauth:2.0:oob")

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

