FROM python:3.7

ENV APP_PATH /opt/apps

COPY requirements.txt $APP_PATH/requirements.base.txt
RUN pip install --no-cache-dir -r $APP_PATH/requirements.base.txt

WORKDIR $APP_PATH
