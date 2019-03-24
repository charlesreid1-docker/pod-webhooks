# Captain Hook's Canary

First things first: Captain Hook is the webhook server that
is part of the webhooks docker pod. It receives webhooks
from Github and Gitea and uses them to trigger scrips.
Links to [documentation](https://pages.charlesreid1.com/b-captain-hook)
and [code](https://git.charlesreid1.com/bots/b-captain-hook)
for Captain Hook.

Captain Hook's Canary is a mechanism by which the Captain Hook
webhooks server (running in a docker container) can trigger an action 
on the host machine (running the pod). In this case the action is to
update Captain Hook and restart the docker pod anytime a webhook is
received indicating the Captain Hook repo has changed.

This is done by bind-mounting a host directory at `/tmp/triggers/`
inside the Captain Hook docker container. When Captain Hook receives
a webhook from Github or Gitea that indicates the Captain Hook
repo (<https://git.charlesreid1.com/bots/b-captain-hook> or
<https://github.com/charlesreid1/captain-hook>), it creates a
trigger file.

Meanwhile, on the host that is running the docker pod, a service 
script is running continuously to check for that trigger file
every 10 seconds. If the trigger file is seen, it updates the
Captain Hook git repository on the host machine and then restarts
the docker pod.

Sections below cover the following scripts, all run on the host:

* The canary bash script
* The docker host pull script
* The canary statup service

## The Canary Bash Script

Note: this needs an associated systemd service.
See the services directory of the dotfiles repo.

This is a canary script for connecting
the Captain Hook container to the host 
machine, and triggering tasks on the 
host machine with webhooks.

The Captain Hook container mounts the 
following host directory inside the 
container (same location for host/container):

```
/tmp/triggers/
```

When a webhook in Captain Hook wants to 
trigger an event on the host (blackbeard),
it puts a file in `/tmp/triggers/`.

Meanwhile, on the host, this script checks
every 10 seconds for trigger files.

Each webhook can create its own trigger file,
and this script processes each trigger differently.

```bash
#!/bin/bash

TRIGGER="/tmp/triggers/push-b-captain-hook-master"
UPDATE_SCRIPT="${HOME}/pod-webhooks/scripts/captain_hook_pull_host.py"

while true
do
    # bootstrap-pull captain hook
    if [ -f "$TRIGGER" ]; then
        echo "CAPTAIN HOOK'S CANARY:"
        echo "Running trigger to update Captain Hook on the host machine (user charles)"
        sudo -H -u charles python $UPDATE_SCRIPT
        echo "All done."
        rm -f ${TRIGGER}
    fi

    sleep 10;
done
```


## The Pull Host Captain Hook Script

Next we have a python script that actually updates the host's 
version of Captain Hook:

```python
#!/usr/bin/env python3
import subprocess
import os
import time

"""
Captain Hook: Pull Captain Hook on the Host 

This script is called by the host machine 
(blackbeard) running the Captain Hook container.

This is triggered by push actions to the 
master branch of b-captain-hook.

The action is to update (git pull) the copy 
of Captain Hook running on the host, and
restart the container pod.
"""

work_dir = os.path.join('/home','charles','pod-webhooks','b-captain-hook')

# Step 1:
# Update Captain Hook
pull_cmd = ['git','pull','origin','master']
subprocess.call(pull_cmd, cwd=work_dir)

time.sleep(5)

# Step 2:
# Restart Captain Hook pod
pod_restart = ['docker-compose','restart']
subprocess.call(pod_restart, cwd=work_dir)
```

## The Canary Startup Script

Here is the startup file that runs the Captain Hook's Canary bash script.

The stop directive uses pgrep to find the process id and stops any PIDs returned.

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

See [Services](services.md) for more info on what to do with this file.


