#!/bin/bash


until PGPASSWORD=123456 psql -h "db-test" -U "postgres" -c '\q'; do
  >&2 echo "Postgres TEST-DB is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres TEST-DB is up - executing command"
pytest > ./test_log.txt

until PGPASSWORD=123456 psql -h "db" -U "postgres" -c '\q'; do
  >&2 echo "Postgres PRODUCTION is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres PRODUCTION is up - executing command"
python -m workshop