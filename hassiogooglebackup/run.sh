#!/bin/sh


OPTIONS_PATH=/data/options.json

GB_DEBUG="$(jq --raw-output '.debug' $OPTIONS_PATH)"
GB_VERSION="1.7.0"

echo "GB_DEBUG = $GB_DEBUG"
echo "GB_VERSION = $GB_VERSION"

export GB_DEBUG
export GB_VERSION

cd googlebackup
python manage.py runserver --noreload 172.30.32.2:8099