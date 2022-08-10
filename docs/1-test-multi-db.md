## Testing Multiple Databases

The state of the application at the moment uses the following packages:

1. django.contrib.admin
2. django.contrib.auth
3. django.contrib.contenttypes
4. django.contrib.sessions
5. django.contrib.messages

Each has its own information to store in a set of database tables.

## Running migrations

From the venv prompt:

```console
py manage.py migrate
```

If you look at the `db.sqlite3` you will see the following tables:

1. acmeapp_post
2. auth_group
3. auth_group_permissions
4. auth_permission
5. auth_user
6. auth_user_groups
7. auth_user_user_permissions
8. django_admin_log
9. django_content_type
10. django_migrations
11. django_session
12. sqlite_sequence

## Switch to multiple database

Let's use two databases and do away with the default database connection.  We will use routers to decide which database to goto for a particular model that is consumed in code.

### Change Database Settings

Change database settings to:

```python
DATABASES = {
    'default': {},
    'auth_db': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'auth_db.sqlite3',
    },
    'acmeapp_db': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'acmeapp_db.sqlite3',
    }
}
```

Here we are no longer using the default database.  Everything will be routed to the aliased db from the routers which we will define next.

### Add Routers

Create a new file under `core` named `db_routers.py`.  This will have 2 classes - a router for Auth - and a router for the AcmeApp.

```python
class AuthRouter:
    route_app_labels = ['auth', 'contenttypes', 'sessions', 'admin']

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'auth_db'

        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'auth_db'

        return None

    def allow_relation(self, obj1, obj2, **hints):
        if (
                obj1._meta.app_label in self.route_app_labels or
                obj2._meta.app_label in self.route_app_labels
        ):
            return True

        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            return db == 'auth_db'
        return None
    
    
class AcmeAppRouter:
    route_app_labels = ['acmeapp']

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'acmeapp_db'

        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'acmeapp_db'

        return None

    def allow_relation(self, obj1, obj2, **hints):
        if (
                obj1._meta.app_label in self.route_app_labels or
                obj2._meta.app_label in self.route_app_labels
        ):
            return True

        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            return db == 'acmeapp_db'
        return None
```

### Configure Routers

In the `core/settings.py` add the following code:

```python
DATABASE_ROUTERS = [
    'core.db_routers.AuthRouter',
    'core.db_routers.AcmeAppRouter'
]
```

### Run migrations

We need to run the migrations using parameterised commands.  These will specify target database to apply migrations to - and it will use the routers to decide which tables to manipulate from the models (and migrations).

If we attempt to migrate with the command `py manage.py migrate` then we will recieve an error indicating that `settings.DATABASES is improperly configured. Please supply the ENGINE value. Check settings documentation for more details.`.  

This is caused by the default database having no configuration.  Unfortunately the `default` alias is required - even though it will never be used.

```python
py manage.py migrate --database=auth_db
py manage.py migrate --database=acmeapp_db
```

### Run test

Fails with:

`django.test.testcases.DatabaseOperationForbidden: Database queries to 'acmeapp_db' are not allowed in this test. Add 'acmeapp_db' to acmeapp.tests.model.TestModels.databases to ensure proper test isolation and silence this failure.`

```python
py manage.py test
```

```
py manage.py runserver
```

## Links

<https://www.youtube.com/watch?v=g-FCzzzjBWo&t=1023s>  
