#!/bin/bash

GOOBOOK_FILE="/var/cloudbackups/workdir/google_contacts.xml"
/usr/local/bin/goobook dump_contacts > "$GOOBOOK_FILE"
gzip -f "$GOOBOOK_FILE"