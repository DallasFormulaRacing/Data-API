# DFR (Dallas Formula Racing) DATA-API

Codebase of the in-house data storage and serving API of [Dallas Formula Racing](https://dallasformularacing.com/).

![](https://img.shields.io/github/last-commit/DallasFormulaRacing/Data-API/main?label=Last+Updated) ![](https://img.shields.io/github/issues/DallasFormulaRacing/Data-API?label=Issues) ![](https://img.shields.io/github/license/DallasFormulaRacing/Data-API?label=License)

## Table of contents

- [DFR (Dallas Formula Racing) DATA-API](#dfr-dallas-formula-racing-data-api)
  - [Table of contents](#table-of-contents)
  - [Current scope of the project](#current-scope-of-the-project)
  - [Local development](#local-development)
    - [Cloning the repo](#cloning-the-repo)
    - [Setting up the virtual environment](#setting-up-the-virtual-environment)
    - [Making a `.env` file](#making-a-env-file)
    - [Running the API locally](#running-the-api-locally)
  - [Logging](#logging)
    - [`.log` file format](#log-file-format)
  - [Advanced development](#advanced-development)
    - [Testing the Docker image](#testing-the-docker-image)
    - [Building the Docker image](#building-the-docker-image)
    - [Starting a container](#starting-a-container)
  - [Endpoints](#endpoints)
    - [`/`](#)
    - [`/upload`](#upload)
      - [Status Codes](#status-codes)
    - [`/download`](#download)
      - [Status Codes](#status-codes-1)


## Current scope of the project

Despite its simple name, this project aims to be the backbone of all current and future software products made within/for DFR, along with being the "one-stop shop" for any and all testing session data and beyond.

However, for the current scope, the project is intended to be a learning ground for "newer" members to get acquainted interacting with APIs in the real world, along with giving a practical example of APIs as a technology.

As of current, this API is purely a method of "file storage" for past and upcoming testing sessions.

Hopefully, in due time, this API will serve as the method for ingesting and distributing all testing data, in various formats, to and from our engineers for their research purposes. Along with serving as a method for consolidating and differentiating between various forms of data, and testing runs.

## Local development

**DISCLAIMER**

This guide assumes you have Python 3.11.X installed, this can be done [here](https://www.python.org/downloads/) (As of writing, 14 September 2024, the latest version with an installer is [v3.11.9](https://www.python.org/downloads/release/python-3119/))

### Cloning the repo

As for all projects on GitHub you need to start by cloning the repo using [git](https://git-scm.com/downloads). You can do this by installing [git](https://git-scm.com/downloads) from the provided link, opening your command line of choice and running the following command.

```shell
git clone https://github.com/DallasFormulaRacing/Data-API.git
```

 This will create a new directory in the location where you ran the command, of which the content of the repository will be located.

### Setting up the virtual environment

Unlike all other projects currently maintained by DFR, this project uses [Pipenv](https://pipenv.pypa.io/en/latest/) to create and manage its virtual environment. What this means is you won't have to worry about managing your `pip` installs and your `virtualenv` separately from each other.

To begin, open your command line of choice and execute the following command `pip install --user pipenv`.

Once you have [Pipenv](https://pipenv.pypa.io/en/latest/) on your machine, you can create an instance of the project's virtual environment by selecting the directory (on Windows you can do this by running the command `cd .\DATA-API\` ), and running the command `pipenv install`.

### Making a `.env` file

Depending on your level of experience, you may or may not have ever used **environment** variables. A `.env` or `.venv` file is in most cases our way of defining these types of variables. For the use case of this project, we will be making a `.env` file, as these are automatically loaded by [Pipenv](https://pipenv.pypa.io/en/latest/) on runtime. 

First create a new file in the root directory of your local repository instance, named `.env`. Once you have this file, open it in your IDE of choice and add the following variables to it, then save the file. If needed, there is an example `.env` file included at the bottom of this section.

* `MONGO_CONNECTION_STRING` -  The connection string to the MongoDB instance, (if you don't have one, you can host your own instance through MongoDB.)

**Example `.env` file**

```shell
MONGO_CONNECTION_STRING = "MONGO CONNECTION STRING HERE BETWEEN THE QUOTES"
```

### Running the API locally

The "fail-proof" method of starting a local instance is by using the following command.
```shell
pipenv run uvicorn app.main:app --host 0.0.0.0 --port 8100 --reload
```
However, if you choose to 'activate' the virtual environment in your IDE of choice (**VS Code** and others do this automatically), then this command is simplified to the below command. (run this from within your IDE's command line.)

```shell
uvicorn app.main:app --host 0.0.0.0 --port 8100 --reload
```

* `pipenv run` Is the base command used to "run" any given command following the statement within the installed virtual environment.
* `uvicorn` Is the web server package that is being used to host the application.
* `app.main:app` Tells `uvicorn` how to find our code, `app.main` being the path to our source code (the `main.py` file in the `app` folder), and `:app` refers to the `app` defined within.
* `--host 0.0.0.0` This flag is used to bind the local server to the IP `0.0.0.0`, which is otherwise known as `localhost`. If you ever want to make a request to your local instance, it should be formatted to this address. For example you can open your browser and navigate to `localhost:8100` in your search bar, this will open the `root` or "home" page of the API.
* `--port 8100` This flag forces our local instance to be hosted on the **TCP** port 8100, and results in the `:8100` being tacked onto our `localhost` address as mentioned above.
* `--reload` This flag is used to tell our web server, `uvicorn`, that we want to reload our local instance every time we make a change to its source code automatically, instead of having to manually stop and restart our local instance. (note, this does not reliably monitor for dependency changes, I.E. any changes to your Pipfile, or to your `.env` file)

Once you have a local instance of the API up and running, you can connect to it by visiting [http://localhost:8100](http://localhost:8100) in your browser, or by exploring some of the example code found in the repository under the `examples` folder [here](https://github.com/DallasFormulaRacing/Data-API/tree/main/examples).

## Logging

All logging for this project is handled with [Python](https://www.python.org/)'s native [logging](https://docs.python.org/3/library/logging.html) library. What this means for newer developers is that all of the output that you would normally see within the console when running the application will instead be saved to a file stored in the `./logs` directory. (If you do not have a `./logs` directory, it is because you have not opened an instance of the API locally yet. Once you do this the directory should be created and all of your logs will be put there.)

### `.log` file format

All `.log` files will follow the naming scheme of `YYYY-MM-DD.log`. Of which within you will find all the information logged on runtime of the API in the following format.

`YYYY-MM-DD HH:MM:SS,MS - LEVEL 0 - LOG CONTENT`

If you ran multiple instances within a single day, or made changes to the API while it was running (assuming you used the `--restart` flag mentioned [here](#running-the-api-locally)), then you will see a breakpoint between each individual instance's log. Which looks like the below example.

```SHELL
YYYY-MM-DD HH:MM:SS,MS - INFO - ---------- STARTING API ----------
```

## Advanced development

### Testing the Docker image

This API is 'published' to a K8s (Kubernetes) environment via a [Docker](https://www.docker.com/) image. In some cases being able to use this environment locally is helpful for troubleshooting. For most though these steps are more involved than are needed for any kind of local development. 

However if you're interested in learning, I highly recommend looking at the [Docker documentation](https://docs.docker.com/) to learn how to fully utilize [Docker](https://www.docker.com/).

**DISCLAMER** 

This short guide assumes that you have [Docker](https://www.docker.com/) installed in some form, I recommend installing [Docker Desktop](https://www.docker.com/products/docker-desktop/) as it makes the whole experience of managing and dealing with multiple containers / builds much easier than strictly through the command line.

### Building the Docker image

Just run the following command in the root directory of your local repository.

```shell
docker build -t data_api .
```

Note, that the first time you run this command it will take some time for [Docker](https://www.docker.com/) to build out the first instance of the API, however, subsequent builds will take substantially less time.

Also note that every time you make a change to the source code of the API, it is **REQUIRED** that you build a new [Docker](https://www.docker.com/) image, otherwise, the changes will not take effect within the K8s environment.

### Starting a container

Again like above, just run the following command and your [Docker](https://www.docker.com/) container should start up.

```shell
docker run -d --name api_container -p 8100:8100 data_api
```

At this point you can now access the locally hosted API by connecting to [http://localhost:8100](http://localhost:8100)


## Endpoints

If you would like a less verbose, and more technical explanation of the endpoints and their functions, please consult the `/docs` endpoint of the API for the automatically generated [Swagger](https://swagger.io/tools/swagger-ui/) documentation. (Note, the docs on the `/docs` endpoint are **NOT** fully automatically generated, there is still developer defined comments and schemas that provide much of the content of the documentation.)

### `/`

The `/` endpoint, also known as the root endpoint, is used for checking if an instance of the API is alive. If calling this endpoint does not return the below JSON snippet, then the API instance did not properly initialize.

```JSON
{"Status": "Ok"}
```

### `/upload`

The `/upload` endpoint should be called when attempting to upload a file to the API for processing/storage within the Mongo database.

It should be noted that a properly formatted request to this endpoint should include both utilization of the **POST** method along with passing a **CSV** file as "file" within the body of the request. An example of how to do this in [Python](https://www.python.org/) can be found [here](https://github.com/DallasFormulaRacing/Data-API/blob/main/examples/example_upload.py). (Due to the nature of FastAPI, it is **REQUIRED** that the file to be uploaded be passed as "file" to match the variable definition found within the function definition for this endpoint [here](https://github.com/DallasFormulaRacing/Data-API/blob/main/app/main.py). This does **NOT** mean that the file needs to be named "file" just that it should be passed as "file" within the request.)

#### Status Codes

This endpoint can return two possible responses, one if the request succeeded, and another if the request failed in some shape or form. Below are example responses of these two responses.

**Status Code 201**

```JSON
{
  "message": "Success uploading {UPLOADED FILENAME} to Mongo"
}
```

**Status Code 500**

```JSON
{
  "message": "Error uploading or processing file."
}
```

### `/download`

The `/download` endpoint should be called when a user wants to pull a specific dataset from the Mongo database. (It is planned to add future support for multiple filetypes, however, at the moment this endpoint will only return CSV data.)

When making a request to the `/download` endpoint make sure that you are using the **GET** method, along with passing the needed headers (listed below).

|header|expected value(s)|required?|
|:---:|:---:|:---:|
|`filename`|The name of the file to be found. (**Includes extension**)|![](https://img.shields.io/static/v1?label=&message=Yes&color=ff0000)|

(More headers will be added in the future as more features are added to the endpoint.)

#### Status Codes

This endpoint can return two possible responses, one if the request succeeded, and another if the request failed in some shape or form. Below are example responses of these two responses.

**Status Code 200**

```JSON
{
  "data": string,
  "format": string
}

```

**Status Code 500**

```JSON
{
  "message": "Error processing file for download."
}
```