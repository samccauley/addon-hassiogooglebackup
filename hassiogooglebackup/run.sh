#!/bin/sh


CONFIG_PATH=/data/options.json
GB_DEBUG="$(jq --raw-output '.debug' $CONFIG_PATH)"

echo "GB_DEBUG = $GB_DEBUG"

cd googlebackup
python manage.py runserver 0.0.0.0:8000