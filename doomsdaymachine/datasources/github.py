from github import Github
import os.path as path
import os
import base64
import urllib.request
from doomsdaymachine.util import format_filename
from doomsdaymachine.sync_map2 import SyncMap2


def execute_github(logger, config, job):
    gclient = Github(job["options"]["access_token"])
    download_github_repositories(logger, job, gclient)
    download_github_gists(logger, job, gclient)
    
def download_github_repositories(logger, job, gclient):
    logger.info("Getting repositories")
    projects_folder = path.join(job["output_folder"], "repositories")
    syncer = SyncMap2(job)
    if not path.isdir(projects_folder):
        os.mkdir(projects_folder)
    for repo in gclient.get_user().get_repos():
        project_file = path.join(projects_folder, repo.full_name)
        if not os.path.isdir(project_file):
            os.makedirs(project_file)
        for branch in repo.get_branches():
            key = repo.full_name + "/" + branch.name
            signature = branch.commit.commit.tree.sha
            if syncer.get_signature(key) != signature:
                logger.info(f"Getting repo {repo.full_name} {branch.name}")
                archive_url = repo.get_archive_link("tarball", branch.name)
                archive_file = path.join(project_file, format_filename(branch.name) + ".tar.gz")
                print(archive_url, archive_file)
                with urllib.request.urlopen(archive_url) as dl_file:
                    with open(archive_file, "wb") as out_file:
                        out_file.write(dl_file.read())
                syncer.set_signature(key, signature)
                syncer.save()

def download_github_gists(logger, job, gclient):
    logger.info("Getting gists")
    gists_folder = path.join(job["output_folder"], "gists")
    if not path.isdir(gists_folder):
        os.mkdir(gists_folder)
    for gist in gclient.get_user().get_gists():
        logger.info(f"Getting gist {gist.id}")
        gist_folder = path.join(gists_folder, gist.id)
        if not path.isdir(gist_folder):
            os.mkdir(gist_folder)
        files = gist.files
        for file_name in files:
            logger.debug(f"Downloading {file_name}")
            file_path = path.join(gist_folder, file_name)
            with open(file_path, "w") as file_handle:
                logger.debug(f"Saving {file_name}")
                file_handle.write(files[file_name].content)
