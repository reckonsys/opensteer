psql -d postgres -c "DROP DATABASE opensteer;"
psql -d postgres -c "CREATE DATABASE opensteer;"
./manage.py migrate
./manage.py loaddata fixtures/data.json
