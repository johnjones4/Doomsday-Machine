# Doomsday Machine

## About

Doomsday Machine is a tool for backing up cloud services to a local machine. This project is a followup to a [Node.js project I started in April](https://github.com/johnjones4/Doomsday-Machine). While that project worked well, I wasn't happy with the code's performance and lack of support, being that the project was just my code. Instead, I've constructed this project which is really just an amalgamation of others' great projects.

## Installation

### Docker Setup

I've not published this project as a Docker image yet, so you must build the image yourself. To do that, run:

```bash
# docker build ./ -t cloud-backup
```

To setup a folder structure on your host machine that you can later map to some key directories on the Docker image, create the following:

* `/var/backup`
* `/var/backup/workdir` - Uncompressed backup data.
* `/var/backup/archives` - Date-stamped backup archives.
* `/var/backup/lastpass` - LastPass CLI configuration
* `/var/backup/geeknote` - GeekNote configuration
* `/var/backup/imap` - IMAP Backup configuration
* `/var/backup/rclone` - RCLone configuration
* `/var/backup/conf` - Goobook and Todoist configurations

### Services Setup

The project is made up of various projects, each with their own configuration system. The benefit of this is that we are relying on popular community tools for backing up services meaning that the support base and reliability for each tool is theoretically higher. The downside is that you must configure each service a little bit differently. For many of these, the easiest way to generate the configuration is to run the docker image and then start up a Bash shell for the running image and use each backup tool's command line based tools to log in. (To do that, see the [Use](#use) section.)

#### IMAP / Email

The _imap-backup_ tool uses a configuration file saved at `/root/.imap-backup/config.json`, which is setup as a Docker volume so that you can persist the configuration and/or map it to a host folder. Use the tool's [setup instructions](https://github.com/joeyates/imap-backup) to build the configuration file.

#### Geeknote / Evernote

Geeknote requires a login from the command line and cannot be configured with just a configuration file. Visit the project's [site](https://github.com/jeffkowalski/geeknote) to see how to login. (Skip all installation steps and proceed to login/authentication steps.) Note that it is best to run these commands from a Bash shell within the running image. The tool's configuration directory, `/root/.geeknote`, is also setup as a Docker volume so that you can persist the configuration and/or map it to a host folder.

#### RClone / Cloud Storage (Google Drive, Dropbox, etc)

RClone requires a login from the command line and cannot be configured with just a configuration file. Visit the project's [site](https://rclone.org) to see how to configure each cloud service. (Skip all installation steps and proceed to login/authentication steps.) Note that it is best to run these commands from a Bash shell within the running image. The tool's configuration directory, `/root/.config/rclone`, is also setup as a Docker volume so that you can persist the configuration and/or map it to a host folder. When starting up the Docker image, you must also set an environment variable named `RCLONE_REMOTES` that specifies the name of each RClone remote you wish to backup separated by `:`. (ex. `RCLONE_REMOTES="GoogleDrive:Dropbox"`)

#### GooBook / Google Contacts

GooBook requires a login from the command line and cannot be configured with just a configuration file. Visit the project's [site](https://gitlab.com/goobook/goobook) to see how to login using the `goobook authenticate` command. (Skip all installation steps and proceed to login/authentication steps.) Note that it is best to run these commands from a Bash shell within the running image. The tool's configuration directory, `/root/.goobookrc`, is also setup as a Docker volume so that you can persist the configuration and/or map it to a host folder.

#### Todoist

Todoist simply requires a _Test token_ from the [Todoist API App Console](https://developer.todoist.com/appconsole.html). To create one, setup a new app in the App Console, and copy the test token into a file named `todoist.json` in a directory on your host machine that you've mapped to `/etc/cloudbackup` in the Docker image:

```JSON
{
  "token": "<TOKEN>",
  "backupPath": "/var/cloudbackups/workdir/todoist.zip"
}
```

#### GitHub

This requires no authentication details because the backup only downloads public repositories. Just set an environment variable when you run the Docker image that specifies the GitHub user to back up. (ex. `GITHUB_USER="johnjones4"`)

#### LastPass

LastPass requires a login from the command line and cannot be configured with just a configuration file. Visit the project's [site](https://github.com/lastpass/lastpass-cli) to see how to login. (Skip all installation steps and proceed to login/authentication steps.) Note that it is best to run these commands from a Bash shell within the running image. The tool's configuration directory, `/root/.lpass`, is also setup as a Docker volume so that you can persist the configuration and/or map it to a host folder.

## Use

### Starting Up

To start up the Docker image, it is best to create a startup script that preserves all environment variables and directory mappings. Here is an example:

```bash
#!/bin/bash

VOL_ROOT="/var/backup"

docker run \
  -d \
  --env RETENTION_DAYS=5 \
  --env RCLONE_REMOTES="GoogleDrive:Dropbox" \
  --env GITHUB_USER="johnjones4" \
  -v $VOL_ROOT/workdir:/var/cloudbackups/workdir \
  -v $VOL_ROOT/archives:/var/cloudbackups/archives \
  -v $VOL_ROOT/lastpass:/root/.lpass \
  -v $VOL_ROOT/geeknote:/root/.geeknote \
  -v $VOL_ROOT/imap:/root/.imap-backup \
  -v $VOL_ROOT/rclone:/root/.config/rclone \
  -v $VOL_ROOT/conf:/etc/cloudbackup \
  cloud-backup
```

### Getting a Bash Shell

To get into a Bash shell on the running Docker image, first run `docker ps` to see a list of running images. Find the row for `cloud-backup` and copy the hash for `CONTAINER ID`. Then run the following: `docker exec -it <CONTAINER ID> bash`.
