#!/bin/sh


OPTIONS_PATH=/data/options.json

GB_DEBUG="$(jq --raw-output '.debug' $OPTIONS_PATH)"
GB_VERSION="1.7.0"

auth_header="X-HASSIO-KEY: ${HASSIO_TOKEN}"

json_info=$(curl -s -H "${auth_header}" 'http://hassio/addons/self/info')

INGRESS_IP=$(echo ${json_info} | jq -r '.data.ip_address')
INGRESS_PORT=$(echo ${json_info} | jq -r '.data.ingress_port')
INGRESS_ENTRY=$(echo ${json_info} | jq -r '.data.ingress_entry')

echo "GB_DEBUG = $GB_DEBUG"
echo "GB_VERSION = $GB_VERSION"

if $GB_DEBUG; then
    echo "Here is the output from /addons/self/info"
    curl -s -H "${auth_header}" 'http://hassio/addons/self/info'
    echo -e "\nEnd of output from /addons/self/info"
    echo "INGRESS_IP = $INGRESS_IP"
    echo "INGRESS_PORT = $INGRESS_PORT"
    echo "INGRESS_ENTRY = $INGRESS_ENTRY"
fi

export GB_DEBUG
export GB_VERSION

cd googlebackup

python manage.py runserver --noreload 0.0.0.0:8000

export INGRESS_ENTRY
python manage.py runserver --noreload $INGRESS_IP:$INGRESS_PORT