echo "######################################"
echo "# Inicializando script para gerar BD #"
echo "######################################"

#wait for the SQL Server to come up
mssql_ready () {
    /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P !MSSQL2017_sophia -Q "SELECT 1" > /dev/null 2>&1
}
until mssql_ready; do
  >&2 echo 'Waiting for MSSQL to become available...'
  sleep 1
done
>&2 echo 'MSSQL is available'

#run the setup script to create the DB and the schema in the DB
/opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P !MSSQL2017_sophia -i setupdb.sql
