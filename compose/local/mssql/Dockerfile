FROM mcr.microsoft.com/mssql/server:2017-latest


# Create directory
RUN mkdir -p /usr/src/db
WORKDIR /usr/src/db

# source
COPY ./compose/local/mssql /usr/src/db
RUN chmod +x /usr/src/db/createdb.sh

# Default SQL Server TCP/Port.
EXPOSE 1433

CMD /bin/bash ./entrypoint.sh
