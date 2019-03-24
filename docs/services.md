## Running Hooks-Subdomains Docker Pod as Startup Service

The webhooks-subdomains docker pod requires two startup
services:

* Docker pod service - this startup service keeps the pod running, 
  and will restart it if it crashes

* Captain Hook's canary - this watches a folder that is shared between
  the docker pod host and the Captain Hook container, which allows the
  pod to send triggers to the host.

Also see the `scripts/` folder of this repo,
[pod-webhooks](https://git.charlesreid1.com/docker/pod-webhooks)
([Github mirror](https://github.com/charlesreid1-docker/pod-webhooks)).


### Docker Pod Startup Service

This service keeps the webhooks docker pod service running
continuously. If the pod stops, this service will restart it.

(This service should not be running if you are troubleshooting
the docker pod, otherwise every time you try and stop the pod
it will respawn.)

**`pod-webhooks.service:`**

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


### Captain Hook's Canary Startup Service

This service just watches a folder for a particular
watchfile, and runs a script if it sees the watchfile
appear.

**`captain-hook-canary.service:`**

```
[Unit]
Description=captain hook canary script
Requires=pod-webhooks.service
After=pod-webhooks.service

[Service]
Restart=always
ExecStart=/home/charles/pod-webhooks/scripts/captain_hook_canary.sh
ExecStop=/usr/bin/pgrep -f captain_hook_canary | /usr/bin/xargs /bin/kill 

[Install]
WantedBy=default.target
```

### Installing Services

Install the services by copying the `*.service` files 
to `/etc/systemd/system/dockerpod-webhooks.servce`
and `/etc/systemd/system/captain-hook-canary.servce`,
and activate the startup services:

```
sudo systemctl enable pod-webhooks.service

sudo systemctl enable captain-hook-canary.service
```

Now you can start/stop the services with:

```
sudo systemctl (start|stop) pod-webhooks.service

sudo systemctl (start|stop) captain-hook-canary.service
```

As mentioned above, these services should be stopped before
doing a `docker-compose stop` or a `docker-compose up --build`
to keep the pod from respawning in the middle of the task.


