# Agency Hub

A resource hub for a community of transit agencies [prototype]

## Dummy data

To reset the database to the dummy data fixture, run the following.

``` bash
dropdb agency-hub # If it already exists
createdb agency-hub
python manage.py migrate
python manage.py loaddata fixtures/dummy_data.json

python manage.py createsuperuser # optional, follow the prompts
```

Make any desired changes and then run the following:

``` bash
python manage.py dumpdata user metabase agency --indent 2 > fixtures/dummy_data.json
```
