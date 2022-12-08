# Team *Reggie* Small Group project

## Team members
The members of the team are:
- *ALI ALKHARS*
- *ABDIRAHMAN AHMED*
- *ILIA JAMASB*
- *CHIN WAN*
- *AMRA MIRZAZADA*

## Project structure
The project is called `msms` (Music School Management System).  It currently consists of a single app `lessons` where all functionality resides.

## Deployed version of the application
The deployed version of the application can be found at *<http://reggie2.pythonanywhere.com/>*.

## Installation instructions
To install the software and use it in your local development environment, you must first set up and activate a local development environment.  From the root of the project:

```
$ virtualenv venv
$ source venv/bin/activate
```

Install all required packages:

```
$ pip3 install -r requirements.txt
```
Make the database migrations:

```
$ python3 manage.py makemigrations
```

Migrate the database:

```
$ python3 manage.py migrate
```

Create the user groups:

```
$ python3 manage.py create_user_groups
```

Seed the development database with:

```
$ python3 manage.py seed
```

Run all tests with:
```
$ python3 manage.py test
```

*The above instructions should work in your version of the application.  If there are deviations, declare those here in bold.  Otherwise, remove this line.*

## Sources
The packages used by this application are specified in `requirements.txt`

*Declare are other sources here.*

Contains code from the provided Clucker source code

Background images are free, taken from https://www.istockphoto.com/search/search-by-asset?affiliateredirect=true&assetid=154927026&assettype=image&utm_campaign=srp_photos_top&utm_content=https%3A%2F%2Funsplash.com%2Fs%2Fphotos%2Fmusic-background&utm_medium=affiliate&utm_source=unsplash&utm_term=music+background%3A%3A%3A
