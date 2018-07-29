#!/bin/bash

DATE=$(date +"%Y_%m_%d_%H_%M")
ARCHIVE="/var/cloudbackups/archives/$DATE.tar.gz"
tar zcf "$ARCHIVE" "/var/cloudbackups/workdir"
find "/var/cloudbackups/archives" -mtime +"$RETENTION_DAYS" -type f -delete
