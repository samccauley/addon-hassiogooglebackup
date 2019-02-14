#!/bin/sh


CONFIG_PATH=/data/options.json
GB_DEBUG="$(jq --raw-output '.debug' $CONFIG_PATH)"

echo "GB_DEBUG = $GB_DEBUG"

cd googlebackup
if ["$GB_DEBUG" = "true"]; then
    echo "Starting googlebackup add-on in debug mode"
    python manage.py runserver --settings=debug_settings 0.0.0.0:8000
else
    echo "Starting googlebackup add-on in normal mode"
    python manage.py runserver 0.0.0.0:8000
fi