#!/bin/bash

mkdir "/var/cloudbackups/workdir/rclone"
IFS=':' read -r -a RCLONE_REMOTES_ARRAY <<< "$RCLONE_REMOTES"
for RCLONE_REMOTE in "${RCLONE_REMOTES_ARRAY[@]}"
do
  mkdir "/var/cloudbackups/workdir/rclone/$RCLONE_REMOTE"
  /usr/bin/rclone sync "$RCLONE_REMOTE":/ "/var/cloudbackups/workdir/rclone/$RCLONE_REMOTE"
done