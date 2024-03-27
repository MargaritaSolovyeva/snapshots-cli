# snapshots
> A tool to import files into a database with ease!

## Required tools
Docker, Docker Compose 

## Introduction
Current project includes the CLI tool, metadata database, snapshots database & monitoring setup
(Prometheus + Graphana + Prometheus Push Gateway).

> Important: since all components are running inside the docker, please use database service name `postgres_snapshots`
> instead of `localhost` when running snapshots commands, i.e.:
> ```bash
> $ snapshots --database postgres_snapshots:5432 data/snapshot_20230101.csv data/snapshot_20230603.csv
> ```
> You can specify any other database url, provided that it will have the required table `snapshots`.


## Prerequisites
The tool setup will automatically spin up and initialize all required infrastructure 
components (postgres DB instances & telemetry services) and mount `/data` folder to the 
application container. In order to use the CLI tool, follow next two steps: 

Spin up docker compose:

```bash
docker-compose up -d
```

Attach to bash within the application container:
```bash
docker exec -it snapshots bash
```

After this you should be able to use CLI (it will be available by the alias `snapshots`).

## `snapshots` tool usage

### `snapshots import` command
The command loads the csv files into a Postgres database.

Usage:

```
Usage: snapshots import [-hV] --database=<databaseUrl>
                        <files>...
      <files>...   space separated file names to load, e.g.
                     data/snapshot_20230101.csv
      --database=<databaseUrl>
                   database host and port in form host:port

```

### `snapshots list` command
The command lists the snapshots which were imported into the database

Usage:

```
Usage: snapshots list [-hV] [<fileNames>...]
      [<fileNames>...]   (optional) space separated names of the files you want to find information about
```

### `snapshots sync` command
The command starts a watcher on the specified directory which loads new files into database

Usage:

```
Usage: snapshots sync [-hV] [--data-dir=<directory>]
                             --database=<databaseUrl>
      --data-dir=<directory>
                  name of the folder to sync
      --database=<databaseUrl>
                  database host and port in form host:port
```

## Introduction

The goal of this challenge is to see how you approach programming and to serve as a basis for a conversation.

We'll be discussing your solution during our next interview.

## What we want from you

1. You'll have to write a solution to the tasks listed below.
2. When you're done, push the code directly to the Github repository and send us an email.

## Additionnal information

- Timebox. We think you can do this in less than 3 hours without any issue, but if you get stuck, don't spend all your
  weekend on it. These tasks are the basis of a conversation for us.
  Structure your work in a state that you'd be able to pick it up later.
- You can write this in any programming language you like. We prefer Golang, but also use Python internally.
- We expect to be able to run the code on our computers, mostly MacOS / Linux.

---

## Tasks

### Task 1 - Load snapshot into a database

Implement a CLI tool called `snapshots` which loads the csv files found under `data/` into a Postgres database.
```
$ snapshots --database localhost:5432 data/snapshot_20230101.csv data/snapshot_20230603.csv
```

### Task 2 - Snapshot Metadata

Implement a solution which lists the snapshots which were imported into the database.
```
$ snapshots list
# A list of relevant information about imported snapshots should show here.
```
This command should help us understand:
- Which snapshots were imported?
- When were the snapshots imported?
- Is this snapshot file already imported the database?

You are free to design any solution that helps us answer these questions.


### Task 3 - Snapshot Service

Implement a long-running service which continuously imports snapshots into the database:
```
snapshots sync --database localhost:5432 --data-dir data/
```
The service should detect snapshot files added to the `data/` directory after it was launched and load them as well.

You'll get bonus points if you are able to add some basic telemetry!


## Final Words

Complete as much of the challenge as you can. We'll be talking thru your solution in our interview.
