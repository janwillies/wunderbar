FROM python:3-alpine

# http://stackoverflow.com/questions/35397295/pycrypto-for-python3-in-alpine
RUN apk add gcc g++ make libffi-dev openssl-dev --update-cache

RUN pip install --upgrade pip

RUN pip install pyyaml \
    relayr \
    plotly \
    certifi

ADD relayr_ssl.patch /relayr_ssl.patch
ADD relayr_python3.patch /relayr_python3.patch

RUN patch /usr/local/lib/python$(echo $PYTHON_VERSION|cut -d'.' -f1,2)/site-packages/relayr/dataconnection.py -p1 < relayr_ssl.patch
RUN patch /usr/local/lib/python$(echo $PYTHON_VERSION|cut -d'.' -f1,2)/site-packages/relayr/dataconnection.py -p1 < relayr_python3.patch

ADD temperature.py /temperature.py

ENTRYPOINT python /temperature.py
