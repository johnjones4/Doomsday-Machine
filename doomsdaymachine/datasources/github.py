from github import Github
import os.path as path
import os
import base64
import urllib.request

def execute_github(logger, config, job):
    gclient = Github(job["options"]["access_token"])
    # download_github_gists(logger, job, gclient)
    download_github_repositories(logger, job, gclient)
    

def download_github_repositories(logger, job, gclient):
    logger.info("Getting repositories")
    projects_folder = path.join(job["output_folder"], "repositories")
    if not path.isdir(projects_folder):
        os.mkdir(projects_folder)
    for repo in gclient.get_user().get_repos():
        logger.info(f"Getting repo {repo.full_name}")
        project_file = path.join(projects_folder, repo.full_name)
        os.makedirs(project_file)
        for branch in repo.get_branches():
            archive_url = repo.get_archive_link("tarball", branch.name)
            archive_file = path.join(project_file, branch.name + ".tar.gz")
            print(archive_url, archive_file)
            with urllib.request.urlopen(archive_url) as dl_file:
                with open(archive_file, "wb") as out_file:
                    out_file.write(dl_file.read())

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
