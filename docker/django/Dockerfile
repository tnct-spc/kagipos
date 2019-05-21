FROM djangobase

ENV APP_PATH /opt/apps

COPY requirements.txt $APP_PATH/requirements.txt
RUN pip install --no-cache-dir -r $APP_PATH/requirements.txt

WORKDIR $APP_PATH
