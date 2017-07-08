#!/bin/bash

service cron stop

/usr/bin/supervisord
