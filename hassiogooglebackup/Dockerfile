ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

# Install requirements for add-on
RUN apk add --no-cache \
    python3 \
    python3-dev \
    py-pip \
    build-base \
  && python3 -m ensurepip \
  && rm -r /usr/lib/python*/ensurepip \
  && pip3 install --upgrade pip setuptools \
  && ln -sf pip3 /usr/bin/pip \
  && ln -sf /usr/bin/python3 /usr/bin/python \
  && python --version \
  && rm -rf /var/cache/apk/*

COPY googlebackup /googlebackup

RUN pip install -r googlebackup/requirements.txt

# Copy data for add-on
COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]