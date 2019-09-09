#!/bin/sh

OPTIONS_PATH=/data/options.json

GB_DEBUG="$(jq --raw-output '.debug' $OPTIONS_PATH)"

auth_header="X-HASSIO-KEY: ${HASSIO_TOKEN}"
json_info=$(curl -s -H "${auth_header}" 'http://hassio/addons/self/info')

GB_SLUG=$(echo ${json_info} | jq -r '.data.slug')
GB_VERSION=$(echo ${json_info} | jq -r '.data.version')

echo "GB_DEBUG = $GB_DEBUG"
echo "GB_VERSION = $GB_VERSION"

if $GB_DEBUG; then
    echo "Here is the output from /addons/self/info"
    curl -s -H "${auth_header}" 'http://hassio/addons/self/info'
    echo -e "\nEnd of output from /addons/self/info"
    echo "GB_SLUG = $GB_SLUG"
fi

export GB_DEBUG
export GB_VERSION
export GB_SLUG

cd googlebackup
gunicorn -b 0.0.0.0:8000 googlebackup.wsgi:application -k gevent