## Running Hooks-Subdomains Docker Pod as Startup Service

The webhooks-subdomains docker pod requires two startup
services - one keeps the docker pod running, the other
watches a folder shared between the host and container
for signals from the container, and uses that to trigger
updates to the subdomains web content.

Also see the `services/` folder of the
[dotfiles/debian repository](https://git.charlesreid1.com/dotfiles/debian),
repository for the systemd services.


### Service 1: Webhooks Docker Pod

This service keeps the webhooks docker pod service running
continuously. If the pod stops, this service will restart it.

(This service should not be running if you are troubleshooting
the docker pod.)

**`dockerpod-webhooks.service:`**

```
[Unit]
Description=webhooks and subdomains docker pod
Requires=docker.service
After=docker.service

[Service]
Restart=always
ExecStart=/usr/local/bin/docker-compose -f /home/charles/codes/docker/pod-webhooks/docker-compose.yml up
ExecStop=/usr/local/bin/docker-compose  -f /home/charles/codes/docker/pod-webhooks/docker-compose.yml down

[Install]
WantedBy=default.target
```

Now install the service to `/etc/systemd/system/dockerpod-webhooks.servce`,
and activate it:

```
sudo systemctl enable dockerpod-webhooks.service
```

Now you can start/stop the service with:

```
sudo systemctl (start|stop) dockerpod-webhooks.service
```

As mentioned above, stop the serivce with 
`sudo systemctl stop dockerpod-webhooks.service` before
doing a `docker-compose stop` or a `docker-compose up --build`
to keep the pod from respawning in the middle of the task.



