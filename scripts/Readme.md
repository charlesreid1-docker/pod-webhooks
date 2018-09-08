# dockerpod-webhooks scripts

Copy this `dockerpod-webhooks.service` service script to 
`/etc/systemd/system/dockerpod-webhooks.service`:

```
sudo cp dockerpod-webhooks.service /etc/systemd/system/dockerpod-webhooks.service
```

Enable/disable the service:

```
sudo systemctl enable dockerpod-webhooks
sudo systemctl disable dockerpod-webhooks
```

Start/restart/stop the service:

```
sudo systemctl start dockerpod-webhooks
sudo systemctl restart dockerpod-webhooks
sudo systemctl stop dockerpod-webhooks
```

