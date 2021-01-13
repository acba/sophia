FROM python:3.7-slim-stretch

ENV PYTHONUNBUFFERED 1



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
    # psycopg2 dependencies
    && apt-get install -y build-essential gcc python3-dev musl-dev \
    # Pillow dependencies
    && apt-get install -y libjpeg-dev zlib1g-dev libfreetype6-dev liblcms2-dev libtiff-dev tk-dev tcl-dev \
    # CFFI dependencies
    && apt-get install -y libffi-dev \
    # Translations dependencies
    && apt-get install -y gettext \
    # Dependencia para o django ldap
    && apt-get install -y libldap2-dev libsasl2-dev libssl-dev

RUN addgroup --system django
RUN adduser --system --group django

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install --no-cache-dir -r /requirements/production.txt \
    && rm -rf /requirements

COPY ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r//' /entrypoint
RUN chmod +x /entrypoint
RUN chown django /entrypoint

COPY ./compose/production/django/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start
RUN chown django /start

COPY . /app

RUN chown -R django /app

USER django

WORKDIR /app

ENTRYPOINT ["/entrypoint"]
