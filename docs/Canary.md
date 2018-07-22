# Captain Hook's Canary

Captain Hook's Canary is a mechanism by which a docker pod
running a webhook server can send a signal to the host to 
restart the docker pod.

This is done by bind-mounting a host directory at `/tmp/triggers/`
inside the docker container, and when a webhook is received 
from git.charlesreid1.com that indicates there was a change
to Captain Hook, the docker pod creates a trigger file.

The canary bash script, meanwhile, is a bash script that runs 
forever and checks for a trigger file from the docker pod
every 10 seconds.

The pull host Captain Hook script is a script that updates the
Captain Hook git repo on the host machine.

On top of all of that, we also need a startup service that will
actually run the captain hook canary script, and keep it running,
and stop it when we ask it to stop.

Sections below cover:
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

while true
do
    # bootstrap-pull captain hook
    if [ -f "/tmp/triggers/push-b-captain-hook-master" ]; then
        echo "CAPTAIN HOOK'S CANARY:"
        echo "Running trigger to update Captain Hook on the host machine (user charles)"
        sudo -H -u charles python /home/charles/blackbeard_scripts/captain_hook_pull_host.py
        echo "All done."
        rm -f "/tmp/triggers/push-b-captain-hook-master"
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

work_dir = os.path.join('/home','charles','codes','bots','b-captain-hook')

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
Requires=dockerpod-captainhook.service
After=dockerpod-captainhook.service

[Service]
Restart=always
ExecStart=/home/charles/blackbeard_scripts/captain_hook_canary.sh
ExecStop=/usr/bin/pgrep -f captain_hook_canary | /usr/bin/xargs /bin/kill 

[Install]
WantedBy=default.target
```

See [Services](Services.md) for more info on what to do with this file.


