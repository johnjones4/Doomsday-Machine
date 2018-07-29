#!/bin/bash

LASTPASS_FILE="/var/cloudbackups/workdir/lastpasss.csv"
/usr/bin/lpass export > "$LASTPASS_FILE"
gzip -f "$LASTPASS_FILE"