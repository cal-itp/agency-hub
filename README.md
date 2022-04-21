# Agency Hub

A resource hub for a community of transit agencies [prototype]

## Development

First create a .env file in the root directory of this repo with the following values:

```
SECRET_KEY="ANY_LONG_STRING_IS_FINE_FOR_DEVELOPMENT"
METABASE_SECRET_KEY= # get this from dashboards.calitp.org
```

Build the project using docker-compose.

``` bash
docker-compose build
docker-compose exec server python manage.py migrate
docker-compose up
```

The server should now be running at http://agency-hub.localhost:8000

## Dummy data

Dummy data is loaded with a snapshot of agencies.yml from April 2022, 2 dashboards and users with emails `caltrans-admin@example.org`, `agency-vendor@example.org`, `multiagency-vendor@example.org`, `agency-staff@example.org` (their passwords are the part of the email before the @, so `caltrans-admin`, etc).

Load the dummy data via the fixtures file.

``` bash
docker-compose exec server python manage.py loaddata fixtures/dummy_data.json
```

If you want to update the (commit) any changes to the fixtures run the following.

``` bash
docker-compose exec server python manage.py dumpdata user metabase agency --indent 2 > fixtures/dummy_data.json
```

## Features

* The primary app can be accesed via http://agency-hub.localhost:8000 and includes the embedded dashboard and a login view.

* Users, dashboard, and agencencies can be created/edited via the django admin at http://agency-hub.localhost:8000/admin/ (using the dummy data, only caltrans-admin has access to this).

* If a user is added, the users activation email can be viewed in the /admin/mailer/message section of the admin.