## The Docker Compose File

The `docker-compose.yml` file contains all the directives needed
to run a docker pod for captain hook and the subdomains nginx server.

Why use docker-compose instead of docker? 
docker-compose is the preferred way to run multiple containers.

## Running Webhooks-Subdomains Docker Pod from Command Line

Run the pod in the foreground or background by running these
commands from the directory containing `docker-compose.yml`:

```
docker-compose up       # interactive
docker-compose up -d    # detached
```

If you want to rebuild all the containers before running up,

```
docker-compose up --build
```

If you just want to rebuild the containers,

```
docker-compose build
```

To rebuild absolutely everything from scratch,

```
docker-compose build --no-cache
```

***WARNING:*** this will re-download all aptitude packages,
which can be extremely slow. Use with caution.)

You can restart all containers in a pod using the restart command:

```
docker-compose restart
```

***WARNING:*** this will ***NOT*** pick up changes to 
Dockerfiles or to files that are mounted into the container.
This simply restarts the container using the same image 
(in memory) that was previously running, ***without***
getting an up-to-date container image.

## Workflow for Docker Pod Updates

To minimize downtime, use the following workflow:

* Run `docker-compose build` to rebuild the images, leaving the pod running (they are not affected)
* Run `docker-compose down` to bring the pod down
* Run `docker-compose up` to bring the pod up

(Add the `-d` flag to start the docker pod in the background.)

