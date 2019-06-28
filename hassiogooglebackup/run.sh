#!/bin/sh


OPTIONS_PATH=/data/options.json

GB_DEBUG="$(jq --raw-output '.debug' $OPTIONS_PATH)"
GB_VERSION="1.6.2"

echo "GB_DEBUG = $GB_DEBUG"
echo "GB_VERSION = $GB_VERSION"

export GB_DEBUG
export GB_VERSION

cd googlebackup
python manage.py runserver --noreload 0.0.0.0:8000