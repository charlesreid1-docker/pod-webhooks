## Adding Hooks

To add a hook to Captain Hook:

1. Create an executable script in [bots/b-captain-hook](https://git.charlesreid1.com/bots/b-captain-hook)
   on git.charlesreid1.com with the name of the action, the name of the repo (not the owner),
   and the name of the branch in the filename. For example, `push-my-dotfiles-master` would be 
   matched every time I `push` changes to the `master` branch  of any repository named `my-dotfiles`.

2. Add, commit, and push your hook to the master branch of Captain Hook

3. Wait about 15 seconds for the canary script to run (it has to update
   the Captain Hook git repo running on the remote server to the latest version
   and restart the webhooks-subdomains docker pod.)

4. Open the `my-dotfiles` repository on git.charlesreid1.com, go to the
   Settings > Webhooks page, and add a Gitea webhook.

5. Enter info:
    a. Payload URL is the Captain Hook server, which is `https://hooks.charlesreid1.com/webhook`.
    b. Content type is application/json
    c. Secret is my little secret
    d. Pick what you'd like, I usually go with "just the push event"

6. Save the webhook, then click on the webhook again to open it back up.
   Scroll down to the bottom right and click "Test Delivery". 

You should see a green success sign. If you see a red warning sign:

* ensure webhooks-subdomain pods are running
* ensure port 5000 open in captain hook container and on blackbeard and on aws
* ensure hook has been added to b-captain-hook repository's hooks folder 


