#!/bin/sh


OPTIONS_PATH=/data/options.json

GB_DEBUG="$(jq --raw-output '.debug' $OPTIONS_PATH)"
GB_VERSION="1.7.0"

echo "HASSIO_TOKEN = $HASSIO_TOKEN"
auth_header="X-HASSIO-KEY: ${HASSIO_TOKEN}"
echo "auth_header = $auth_header"

curl -v -H '${auth_header}' 'http://hassio/addons/self/info'

INGRESS_IP="$(curl -s -H '${auth_header}' 'http://hassio/addons/self/info' | jq -r '.ip_address')"

echo "GB_DEBUG = $GB_DEBUG"
echo "GB_VERSION = $GB_VERSION"
echo "INGRESS_IP = $INGRESS_IP"

if $GB_DEBUG; then
    echo "Here is the output from /addons/self/info"
    curl -s -H '${auth_header}' 'http://hassio/addons/self/info'
    echo "End of output from /addons/self/info"
fi

export GB_DEBUG
export GB_VERSION

cd googlebackup
python manage.py runserver --noreload $INGRESS_IP:8099