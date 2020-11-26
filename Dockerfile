FROM python:3.7

ADD . /opt/app
WORKDIR /opt/app
RUN pip install --no-cache-dir -r pip-requirements.txt
CMD [ "python", "./main.py" ]
