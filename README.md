# Mountain Peaks App - v0.3

## Table of Contents

- [App Objectives & Content](#mountain-peaks-app)
  - [Objectives](#objectives)
  - [Content](#content)
- [Prerequisites](#prerequisites)
- [Deploy the app locally](#deploy-the-app-locally-and-run)
- [Change logs](#change-logs)
- [What's next](#what's-next)

## Mountain Peaks App

Demonstrator application for MFI

### Objectives

The features of this application are:

- Provide a **data base** storing basic mountain informations (name, height, latitude, longitude)
- **CRUD** operations on mountain's data
- **Search** for mountains into a geographical area, bounding box-style

### Content

- This an API-only app, there is no frontend stack for the moment

## Prerequisites

Have installed:

- **[Docker Desktop](https://docs.docker.com/get-docker)** - _one of the 3-lastest versions_
- **[Git client](https://git-scm.com/downloads)**

## Deploy the app locally and run

Follow the steps:

1. **Clone** the repo:  
   `git clone https://github.com/nicodfhl/mountain-peaks.git`
1. **Build & Run** the application by running:  
   `cd mountain-peaks`  
   `docker compose up --build`
1. **Open [`http://localhost:80`](http://localhost:80)** in your web browser.
1. Press `CTRL+C` in the terminal to stop the application.

## Use the app

Try the different **entry points** by using the API Swagger UI feature provided by FastAPI to explore, call and test your API directly from the browser **[`http://localhost/docs`](http://localhost/docs)**:

1. Unfold an open point (_right down arrow_)
1. Click on the right button **`Try it out`**
1. If required, fill the request body by inspiring yourself from the request sample given
1. Click on the button **`Execute`** just below
1. Check the _Server response_ success, update your entry if code status is not `200` or `202` and re-execute

_Notice that FastAPI provides an alternative API documentation access with_ **_[`http://localhost/redoc`](http://localhost/redoc)_**

## Change logs

- Version 0.3
  - Develop backend
  - Unittest solution
- Version 0.2
  - Init postgreSQL dB within psycopg (the PostgreSQL client library for python)
- Version 0.1
  - deploy the app to a fully-featured Kubernetes env. - _in progress_
  - add simple backend
  - configure CI/CD (basic)
  - dep management solution with Poetry
  - containerize the app
  - init docker app

## What's next

- use SQLModel lib to simplify the implementation
