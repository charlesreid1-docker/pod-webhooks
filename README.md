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


