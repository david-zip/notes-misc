# Django Development

Django is a framework that helps developers design, create, and deploy websites.

## Getting Started

### Creating a Project

Some code must be initially generated to start any Djago development project; this can be done on your terminal. Change the terminal directory to your desired working space and run the following command:

```bash
django-admin startproject <project_name>
```

After running the above command, you should see a new folder with the name provided. The directory path should look as follows:

```bash
project_name/
    manage.py
    project_name/
        __init__.py
        settings.py
        urls.py
        asgi.py
        wsgi.py
```

The files are:

- Outer **project_name/** root directory which is a container for the project

- **manage.py** is a command line utility that allows you to interact with the Django project

- Inner **project_name/** directory is the actual python package of the Django project

- **project_name/__init__.py** is an empty file that tells python that this directory should be considered as a package

- **project_name/settings.py** is the settings and configuration file for the Django project

- **project_name/urls.py** contains the URL declarations of the project (table of contents of URLs)

- **project_name/asgi.py** is an entry-point for ASGI-compatible web servers to serve the project

- **project_name/wsgi.py** is an entry-point for WSGI-compatible web servers to serve the project

### Development Server

We can verify whether the project is working or not by deploying the website. Change the terminal directory to the website container and run the following command:

```bash
python manage.py runserver
```

If `debug=True` and you have no code, you will see the development page. Otherwise you will see the website you created. The development page is a lightweight web server written purely in python

##### Change the port

By default, the `runserver` command starts the developement server on the interal IP at port 8000.

You can change the servers port by passing it as a command arguement.

```bash
python manage.py runserver 8080
```

If you want to change the servers IP, it can be done doing the following (include the port as well):

``` 
python manage.py runserver 0.0.0.0:8000
```

##### Automatic reloading of ```runserver```

The development server automatically reloads Python code for each request as needed. The server does not have to be restarted for any code changes to take effect. Actions such as adding new files does not trigger a restart and therefore, you would have to trigger the restart manually.

## Creating a Application - Demo

##### Project vs. Apps

An application is a web page that does something. A project is a collection of settings and configurations for applications for a particular website. A project can contain many applications. An application can be in multiple projects.

### Create an Application 

Applications can live anywhere in the Python path. The application can be created in the same directory as the ```manage.py``` file.

```bash
python manage.py startapp <application_name>
```

Directory path of new files will be as follows:

```bash
polls/
    __init__.py
    admin.py
    apps.py
    migrations/
        __init__.py
    models.py
    tests.py
    views.py
```

`include()` function allows for referencing other URLconfs. When Django encounters `include()`, it cuts off whatever part of the URL matched up to that point and sends the remaining string to the included URLconf. 

`include()` makes it easy to plug-and-play URLs. Always use `include()` when you want to include other URL patterns

#### `path()` Function
`path()` function is passed four arguments, two required: **route** and **view**, and two optional: **kwargs** and **name**.

**route** is a string that contains the URL pattern. When processing a request, Django starts at the first pattern in **urlpatterns** and makes its way down the list, comparing the requested URL against each pattern until it finds one that matches.

**view** is what Django will call if it finds a matching pattern. It calls the specfied view function with an HttpRequest object and any captured values from the route.

**kwargs** are any keyword arguments that can be passed in a dictionary to the target view.

**name** allows you to unambigously refer to your URL elsewhere in the Django project.

### Look into `settings.py`
It is a normal python module with module-level variables representing Django settings. 

By default, the configuration uses SQLite (which is included in Python) but you can always change this. You can do so by locating database (looks like below) and changing the variables:

```py
# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

Below are some of the options that be implemented:
- Engine:
  - `django.db.backends.sqlite3`
  - `django.db.backends.postgresql`
  - `django.db.backends.oracle`
  - `django.db.backends.mysql`
- Name - Name of the datbase
  - Default value will be `base_dir / 'db.sqlite3'` and will store the file in the project directory

On the top of `settings.py`, there is a section for `INSTALLED_APPS`. These are the names of the various applications activated in this Django instance. By default, the following applications will be enabled:
- `django.contrib.admin` - Admin site
- `django.contrib.auth` - Authentication site
- `django.contrib.contenttypes` - Framework for content types
- `django.contrib.sessions` - Session framework
- `django.contrib.messages` - Messaging framework
- `django.contrib.staticfiles` - Framework for managing static files

Some of these applications will make use of at least one database so we will need to create the tables i the database. We can do s with the following command:

```bash
python manage.py migrate
```

`migrate` command looks at the `INSTALLED_APPS` settings and creates any necessary database tables according what applications are found.

### Creating Models

Models represent your database layout, with additional metadata. Django follows the DRY principle, which means it prefers that you define your model in one place and automatically derive things from it.

Creating models (no matter how big or small) will provide Django with a lot of information. For example, it tells Django to:
- Create a database schema for the app
- Create a Python database-access API for accessing models

After creating the models, they must be added to the `installed_apps` so Django knows these additionals are ready.

Once the app has been included in the `settings.py`, run the migrate command.