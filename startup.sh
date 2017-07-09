#!/bin/bash

service cron stop

mkdir /root/Dropbox

ln -s /root/Dropbox /var/cloudbackups/workdir/dropbox

/usr/bin/supervisord
