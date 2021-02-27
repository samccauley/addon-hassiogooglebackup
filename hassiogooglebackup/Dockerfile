ARG BUILD_FROM=ghcr.io/hassio-addons/base/amd64:9.1.2
# hadolint ignore=DL3006
FROM $BUILD_FROM

ENV LANG C.UTF-8

# Install requirements for add-on
RUN apk add --no-cache \
    build-base=0.5-r2 \
    jq=1.6-r1 \
    py3-gevent=1.5.0-r1 \
  && python3 -m ensurepip \
  && rm -r /usr/local/lib/python*/ensurepip \
  && pip3 install --no-cache-dir --upgrade pip==20.3.4 setuptools==51.3.3 \
  && ln -sf pip3 /usr/local/bin/pip \
  && ln -sf /usr/local/bin/python3 /usr/local/bin/python \
  && python --version \
  && rm -rf /var/cache/apk/*

COPY googlebackup /googlebackup

# hadolint ignore=DL3003
RUN pip install --no-cache-dir -r googlebackup/requirements.txt \
  && cd googlebackup \
  && python manage.py migrate

# Copy data for add-on
COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]