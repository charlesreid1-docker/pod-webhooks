# pod-webhooks scripts

Copy this `pod-webhooks.service` service script to 
`/etc/systemd/system/pod-webhooks.service`:

```
sudo cp pod-webhooks.service /etc/systemd/system/pod-webhooks.service
```

Enable/disable the service:

```
sudo systemctl enable pod-webhooks
sudo systemctl disable pod-webhooks
```

Start/restart/stop the service:

```
sudo systemctl start pod-webhooks
sudo systemctl restart pod-webhooks
sudo systemctl stop pod-webhooks
```

