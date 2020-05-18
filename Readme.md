# Doomsday Machine

## About

Doomsday Machine is a tool for backing up cloud services to a local machine.

## Installation

TODO

## Setup

The file `config.sample.yml` includes all configurations for the project. Copy that file to `config.yml` and begin updating the file to meet your needs. You may remove or duplicate any job in the list.

### Backup Jobs

#### Dropbox Setup

To setup Dropbox access, go to the [Dropbox App Console](https://www.dropbox.com/developers/apps) and create a new app. After setting up the app (you only need to provide basic information as you'll be the only one consuming this) under "Generated access token", click "Generate." Copy and paste that generated code to the configuration option `oauth2_access_token`. In the Dropbox configuration, you may also specify a whitelist of paths that should be downloaded. Omit that option to download all files.

#### Google Contacts

TODO

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

