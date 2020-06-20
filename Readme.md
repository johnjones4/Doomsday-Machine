# Doomsday Machine

## About

Doomsday Machine is a tool for backing up cloud services to a local machine.

## Installation

To install the main script, run the following:

```sh
$ git clone git@github.com:johnjones4/Doomsday-Machine.git
$ cd Doomsday-Machine
$ make install
```

If you would like to run Doomsday Machine on a schedule, I recommend using something like [Supervisord](http://supervisord.org/) to manage the application. Once you have Supervisord installed for your distro, you can use the following as a template Supervisord configuration for Doomsday Machine. Note that this configuration expects this project to be checked out in the directory `/usr/local/src/Doomsday-Machine/`, it expects a directory for logging named `/var/log/doomsday/`, and it expects a config file at `/var/lib/doomsday/config.yml`.

```
[program:doomsday]
command=/usr/bin/python3 /usr/local/src/Doomsday-Machine/backup.py
directory=/usr/local/src/Doomsday-Machine
autostart=true
autorestart=true
startretries=3
stderr_logfile=/var/log/doomsday/supervisor-backup.err.log
stdout_logfile=/var/log/doomsday/supervisor-backup.out.log
user=root
environment=CONFIG_FILE='/var/lib/doomsday/config.yml'

[program:doomsdaywebserver]
command=/usr/bin/python3 /usr/local/src/Doomsday-Machine/webserver.py
directory=/usr/local/src/Doomsday-Machine
autostart=true
autorestart=true
startretries=3
stderr_logfile=/var/log/doomsday/supervisor-webserver.err.log
stdout_logfile=/var/log/doomsday/supervisor-webserver.out.log
user=root
environment=CONFIG_FILE='/var/lib/doomsday/config.yml'
```

## Setup

The file `config.sample.yml` includes all configurations for the project. Copy that file to `config.yml` and begin updating the file to meet your needs. You may remove or duplicate any job in the list. Specify the absolute path to this file as an environment variable named `CONFIG_FILE`

### Backup Jobs

#### Dropbox Setup

To setup Dropbox access, go to the [Dropbox App Console](https://www.dropbox.com/developers/apps) and create a new app. After setting up the app (you only need to provide basic information as you'll be the only one consuming this) under "Generated access token", click "Generate." Copy and paste that generated code to the configuration option `oauth2_access_token`. In the Dropbox configuration, you may also specify a whitelist of paths that should be downloaded. Omit that option to download all files.

#### Google Contacts

Setup for this data source is a bit more complex. First, create an application on the [Google API Console](https://console.developers.google.com/), give the application access to the _Google People API_, and create Oauth credentials for a Desktop Client.

Now, copy and paste new client credentials into your `config.yml` file as `client_id` and `client_secret` under `options` for the section titled `Google Contacts`. Next, run `make authenticate` which will generate an authorization URL. Open that URL in a browser, agree to give your new application access to your contact, and copy the generated token and paste it as `token`. Now run `make authenticate` one last time, which will result in a `token` and a `refresh_token`. Copy an paste those keys to `token` and `refresh_token` in your `config.yml`.

#### LastPass

To setup LastPass access, specify your username and password in the options.

#### GitHub

To setup GitHub access, go to your [Personal access tokens](https://github.com/settings/tokens), click "Generate new token," and select everything under "repo" under scopes. Copy and paste that generated code to the configuration option `access_token`.

#### IMAP

To add an email/IMAP account, specify all of the standard IMAP connection details as well as a list of mailboxes to download.

### Other Configuration Options

#### Notifications

Upon completion of each backup job, Doomsday Machine can send an email notification. To allow that, specify IMAP connection details under `email_notification`.

#### Delay

Between jobs and run loops, you can specify a delay time (In seconds) under `delay`.

#### Outputs

Doomsday Machine will loop through a list of output directories under `outputs` in case you want to keep multiple redundant backups.

#### Active Job

Doomsday Machine will write a JSON file with the active job information to the path specified in `active_job_file_path`.

#### Logging

To control logging, set a logging level and/or output file under `logging`.
