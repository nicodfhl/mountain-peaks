# Mountain Peaks App - v0.2

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
1. **Open [`http://localhost:8088`](http://localhost:8088)** in your web browser.

## Change logs

- Version 0.1
  - deploy the app to a fully-featured Kubernetes env. - _in progress_
  - add simple backend
  - configure CI/CD (basic)
  - dep management solution with Poetry
  - containerize the app
  - init docker app

## What's next

- Init postgreSQL dB
- Develop backend
- Unittest solution
