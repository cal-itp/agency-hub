# Agency Hub

A resource hub for a community of transit agencies [prototype]

## Development

Build the project using docker-compose.

``` bash
docker-compose build
docker-compose up
```

Load the dummy data via the fixtures file

``` bash
docker-compose exec server python manage.py loaddata fixtures/dummy_data.json
```

If you want to update the (commit) any changes to the fixtures run the following.

``` bash
docker-compose exec server python manage.py dumpdata user metabase agency --indent 2 > fixtures/dummy_data.json
```
