# TEMPORARILY OUT OF SERVICE

4/22/2018

We just got the webhooks server working after a harrowing 
experience with various incarnations of flask servers
running in containers. It currently runs as a one-container
pod, as does the nginx subdomains pod.

Eventually these should be reconciled and this repo should 
contain a combined dockerfile, but right now I'm reluctant
to touch it.

The other thing that should be fixed is the fact that 
we don't want to mount static content inside the container.
We want to bind-mount the static content into both containers.



# pod-webhooks

This docker pod runs two services:

 * Captain Hook webhook server (python + flask)
    * [b-captain-hook](https://git.charlesreid1.com/bots/b-captain-hook)
 * Static content server for subdomain pages (nginx)
    * [d-nginx-subdomains](https://git.charlesreid1.com/docker/d-nginx-subdomains)

 These two services are in this repo as submodules.

## How It Works

Use the docker-compose file to run this docker pod.

## Volumes

This uses one shared volume between the two containers.

Captain Hook updates the static content based on web hooks that it receives,
while the nginx container serves up the static content.

## Servers 

This pod runs on blackbeard.

The nginx service is reverse-proxied HTTP with krash,
and accessible at ports 7777-7779 and up.

The Captain Hook webhook server is also reverse-proxied HTTP.
The krash nginx server will handle all traffic to 
`https://hooks.charlesreid1.com` except URLs prefixed
with `webhook`, which are forwarded on to Captain Hook
on port 5000.


