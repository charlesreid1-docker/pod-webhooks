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

## If you get a 403

If you visit the IP of the page running things and you get a 403,
it's probably because you haven't created the `/www/` directory
structure yet. To do this, you need:

```
/www/pages.charlesreid1.com/
/www/bots.charlesreid1.com/
/www/hooks.charlesreid1.com/
```

