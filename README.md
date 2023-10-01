# Gaant Recipes

Manage and visualize your recipes as projects, with parallelizable time-bounded steps.

## Local Development

In the project root, create a `django_secret.txt` file with a [SECRET_KEY](https://docs.djangoproject.com/en/4.2/ref/settings/#secret-key) string for the project, and then run

```
docker compose up -d
```

If it is the first time you run the project, also apply the db migrations with

```
docker compose exec main bash -c "python manage.py migrate"
```

You will find the app on port `8000`, as in, `http://localhost:8000/` :)
