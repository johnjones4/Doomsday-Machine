#!/bin/bash

OUT_DIR="/var/cloudbackups/workdir"
ARCHIVE_DIR="/var/cloudbackups/archives"
LOG="/var/log/backup.log"

touch "$LOG"

# LastPass

# echo "Backing up LastPass" >> $LOG
# LASTPASS_FILE="$OUT_DIR/lastpasss.csv"
# /usr/bin/lpass export > "$LASTPASS_FILE"
# gzip "$LASTPASS_FILE"
# echo "Done backing up LastPass" >> $LOG

# IMAP

echo "Backing up IMAP" >> $LOG
IMAP_LOCKFILE="/var/run/imap-backup-running"
if [ ! -f $IMAP_LOCKFILE ]; then
  touch "$IMAP_LOCKFILE"
  /root/.rbenv/shims/imap-backup >> $LOG 2>> $LOG
  rm "$IMAP_LOCKFILE"
fi
echo "Done backing up IMAP" >> $LOG

# GeekNote

echo "Backing up Evernote" >> $LOG
GEEKNOTE_LOCKFILE="/var/run/geeknote-running"
if [ ! -f $GEEKNOTE_LOCKFILE ]; then
  touch "$GEEKNOTE_LOCKFILE"
  /usr/local/bin/gnsync --path "$OUT_DIR/evernote" --download-only --all >> $LOG 2>> $LOG
  rm "$GEEKNOTE_LOCKFILE"
fi
echo "Done backing up Evernote" >> $LOG

# RClone

echo "Backing up RClone Services" >> $LOG
RCLONE_LOCKFILE="/var/run/rclone-running"
if [ ! -f $RCLONE_LOCKFILE ]; then
  touch "$RCLONE_LOCKFILE"
  mkdir "$OUT_DIR/rclone"
  IFS=':' read -r -a RCLONE_REMOTES_ARRAY <<< "$RCLONE_REMOTES"
  for RCLONE_REMOTE in "${RCLONE_REMOTES_ARRAY[@]}"
  do
    mkdir "$OUT_DIR/rclone/$RCLONE_REMOTE"
    /usr/bin/rclone sync "$RCLONE_REMOTE":/ "$OUT_DIR/rclone/$RCLONE_REMOTE" >> $LOG 2>> $LOG
  done
  rm "$RCLONE_LOCKFILE"
fi
echo "Done backing up RClone Services" >> $LOG

# GooBook

echo "Backing up Google Contacts" >> $LOG
GOOBOOK_FILE="$OUT_DIR/google_contacts.xml"
/usr/local/bin/goobook dump_contacts > "$GOOBOOK_FILE"
gzip -f "$GOOBOOK_FILE"
echo "Done backing up Google Contacts" >> $LOG

# Todoist Backup

echo "Backing up Todoist" >> $LOG
/usr/bin/todoist-backup --config /etc/cloudbackup/todoist.json
echo "Done backing up Todoist" >> $LOG

# GitHub Backup

echo "Backing up GitHub" >> $LOG
/usr/bin/github-backup "$GITHUB_USER" "$OUT_DIR/github/"
echo "Done backing up GitHub" >> $LOG

# Compress an Archive

echo "Compressing backups" >> $LOG
DATE=$(date +"%Y_%m_%d_%H_%M")
ARCHIVE="$ARCHIVE_DIR/$DATE.tar.gz"
tar zcf "$ARCHIVE" "$OUT_DIR" >> $LOG 2>> $LOG
find "$ARCHIVE_DIR" -mtime +"$RETENTION_DAYS" -type f -delete >> $LOG 2>> $LOG
echo "Done compressing backups" >> $LOG
