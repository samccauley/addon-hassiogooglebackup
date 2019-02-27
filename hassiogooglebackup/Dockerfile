ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

# Install requirements for add-on
RUN apk add --no-cache \
    build-base \
    jq \
  && python3 -m ensurepip \
  && rm -r /usr/local/lib/python*/ensurepip \
  && pip3 install --upgrade pip setuptools \
  && ln -sf pip3 /usr/local/bin/pip \
  && ln -sf /usr/local/bin/python3 /usr/local/bin/python \
  && python --version \
  && rm -rf /var/cache/apk/*

COPY googlebackup /googlebackup

RUN pip install -r googlebackup/requirements.txt \
  && cd googlebackup \
  && python manage.py migrate

# Copy data for add-on
COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]