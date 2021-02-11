FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update \
    && apt-get install -y build-essential gcc python3-dev musl-dev

##
## Necessario para instalar os drivers para o SQL Server
##

RUN apt-get update \
    && apt-get install -y apt-utils curl apt-transport-https wget gnupg \
    # Pacote para o django-pyodbc-azure
    && apt-get install -y unixodbc unixodbc-dev

RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/9/prod.list > /etc/apt/sources.list.d/mssql-release.list

RUN apt-get update \
    && ACCEPT_EULA=Y apt-get install -y --no-install-recommends msodbcsql17 unixodbc-dev \
    && ACCEPT_EULA=Y apt-get install -y --no-install-recommends mssql-tools


RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile \
    && echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc \
    && /bin/bash -c "source ~/.bashrc"


RUN apt-get update \
    # Pillow dependencies
    && apt-get install -y libjpeg-dev zlib1g-dev libfreetype6-dev liblcms2-dev libtiff-dev tk-dev tcl-dev \
    # Git
    && apt-get install -y git \
    # PyAudio
    && apt-get install -y portaudio19-dev python3-pyaudio sox \
    # TextProcessor dependencies
    && apt-get install -y antiword tesseract-ocr ffmpeg \
    # CFFI dependencies
    && apt-get install -y libffi-dev \
    # Translations dependencies
    && apt-get install -y gettext \
    # Dependencia para o django ldap
    && apt-get install -y libldap2-dev libsasl2-dev libssl-dev \
    # cleaning up unused files
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install -r /requirements/local.txt

# COPY ./compose/production/django/entrypoint /entrypoint
# RUN sed -i 's/\r//' /entrypoint
# RUN chmod +x /entrypoint

COPY ./compose/local/django/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start

COPY ./compose/local/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY ./compose/local/celery/beat/start /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat
RUN chmod +x /start-celerybeat

COPY ./compose/local/celery/flower/start /start-flower
RUN sed -i 's/\r$//g' /start-flower
RUN chmod +x /start-flower

WORKDIR /app

# ENTRYPOINT ["/entrypoint"]
CMD ["/start"]
