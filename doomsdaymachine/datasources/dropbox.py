import os
import os.path as path
from dropbox.dropbox import Dropbox
from dropbox.files import FileMetadata, FolderMetadata
import fnmatch
from doomsdaymachine.sync_map import SyncMap


def execute_dropbox(logger, config, job):
    file_output_folder = path.join(job["output_folder"], "files")
    if not path.isdir(file_output_folder):
        os.mkdir(file_output_folder)
    syncer = SyncMap(job)
    client = Dropbox(oauth2_access_token=job["options"]["oauth2_access_token"])
    result = None
    count = 0
    while not result or result.has_more:
        if result and result.cursor:
            logger.debug(f"Continuing query")
            result = client.files_list_folder_continue(result.cursor)
        else:
            logger.debug(f"Performing first query")
            result = client.files_list_folder("", recursive=True, limit=100)
        for file in result.entries:
            if "include" not in job["options"] or is_valid_path(file.path_lower, job["options"]["include"]):
                local_path = path.join(file_output_folder, file.path_lower[1:])
                if isinstance(file, FileMetadata) and file.server_modified.timestamp() > syncer.get_last_modified(file.path_lower):
                    try:
                        logger.debug(f"Downloading: {file.path_lower}")
                        folder = os.path.dirname(local_path)
                        if not path.isdir(folder):
                            os.makedirs(folder)
                        client.files_download_to_file(local_path, file.path_lower)
                        syncer.set_last_modified(file.path_lower, file.server_modified.timestamp())
                        count += 1
                    except:
                        logger.error(f"Exception during {job['type']}/{job['name']} to {job['output_folder']}", exc_info=True)
            else:
                logger.debug(f"Not a match or up to date: {file.path_lower}")
        logger.info(f"Files downloaded: {count}")
        syncer.save()
    syncer.close()


def is_valid_path(path, valids):
    for valid in valids:
        if fnmatch.fnmatch(path, valid):
            return True
    return False


