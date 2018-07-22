# pod-webhooks

This docker pod runs two services:

 * Captain Hook webhook server (python + flask)
    * [b-captain-hook](https://git.charlesreid1.com/bots/b-captain-hook)
 * Static content server for subdomain pages (nginx)
    * [d-nginx-subdomains](https://git.charlesreid1.com/docker/d-nginx-subdomains)

 These two services are in this repo as submodules.

## Links

See documentation page here: <https://pages.charlesreid1.com/pod-webhooks>

Or visit [docs/index.md](/docs/index.md)

Source code on git.charlesreid1.com: <https://git.charlesreid1.com/docker/pod-webhooks>

Source code on github.com: <https://github.com/charlesreid1-docker/pod-webhooks>


## Adding Hooks

Since this is probably the only thing you'll care about once everything
is actually running... until it breaks.

[How To Add A Hook](Adding.md)


## How It Works

See [Running.md](Running.md) for info about running this docker pod.

* Running the Docker Pod from Comand Line
* Workflow for Docker Pod Updates

See [Services.md](Services.md) for info about running startup services.

* Running the Docker Pod as a Startup Service
* Running Captain Hook's Canary (Script)

Enable/disable service (installs/uninstalls, but does not start):

```
sudo systemctl (enable|disable) dockerpod-webhooks.service
sudo systemctl (enable|disable) captain-hook-canary.service
```

Start/stop:

```
sudo systemctl (start|stop) dockerpod-webhooks.service
sudo systemctl (start|stop) captain-hook-canary.service
```

See [Captain Hook's Canary (Canary.md)](Canary.md) for details on the canary script that allows the
webhooks docker pod to trigger itself to be re-loaded when there are new hooks
added to captain hook.


## Volumes and Files

### Subdomains

The static files hosted on charlesreid1.com subdomains are contained in
subdirectories of `/www/*.charlesreid1.com/` and this is
mounted by the subdomains docker container that has rules
set up for which subdomains to serve.

### Captain Hook

Captain Hook mounts the `/www` folder, which is served by the subdomains
nginx server, as well as the hooks folder in the Captain Hook repository
(that's at `b-captain-hook/hooks`).

When there is a change pushed to a particular branch on git.charlesreid1.com,
the git.charlesreid1.com server will check if there is a corresponding hook that's
been added to Captain Hook for that repo and branch. If so, git.charlesreid1.com
runs that script. For pages.charlesreid1.com, that's usually just a git pull 
on the contents of `/www/pages.charlesreid1.com/my-page`.

### Captain Hook's Canary

Captain Hook presents a bit of a paradox: the webhook docker pod needs to be 
able to tell the host to restart the webhook docker pod when changes are pushed
to Captain Hook itself.

This is done by Captain Hook's Canary. This is a script that checks every 10 seconds
for a trigger file in a directory mounted between the host and container. If the 
trigger file is present, the host will update its copy of Captain Hook,
then restart the webhooks-subdomains docker pod.

As per the [`blackbeard_scripts`](https://git.charlesreid1.com/dotfiles/debian/src/branch/master/dotfiles/blackbeard_scripts)
directory of [dotfiles/debian](https://git.charlesreid1.com/dotfiles/debian),
the `captain_hook_canary.sh` canary will restart the webhooks docker pod if it 
detects the file:

```
/tmp/triggers/push-b-captain-hook-master
```

(The canary script will clean up this file.)

Now a hook can be added to Captain Hook that will be run when there is a push event
on the master branch of [bots/b-captain-hook](https://git.charlesreid1.com/bots/b-captain-hook).
By creating a hook named `push-b-captain-hook-master` in the
`hooks/` directory of captain hook that runs a simple `touch` command,
this webhook can trigger the script which triggers a restart of the
docker pod.

Code: <https://git.charlesreid1.com/bots/b-captain-hook/src/branch/master/hooks/push-b-captain-hook-master>


## Network

The `d-subodomains-nginx` container opens different ports for different
subdomains, and reverse-proxies requests from charlesreid1.com.
The port numbering starts at 7777 for pages.charlesreid1.com
and goes up from there, one port per subdomain.

Also see [pod-charlesreid1](https://git.charlesreid1.com/docker/pod-charlesreid1)
on git.charlesreid1.com for the nginx reverse proxy configuration.

Captain Hook runs a Flask server on port 5000 and listens for triggers
from git.charlesreid1.com (gitea) web hooks. These web hooks must have 
the correct secret or the trigger will be ignored.


## Servers 

This pod runs on blackbeard.

The nginx service is reverse-proxied HTTP with krash,
and accessible at ports 7777+ and up.

The Captain Hook webhook server is also reverse-proxied HTTP.
The krash nginx server will handle all traffic to 
<https://hooks.charlesreid1.com> except URLs prefixed
with `webhook`, which are forwarded on to Captain Hook
on port 5000.


