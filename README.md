# Just some setup related stuff for myself

### systemctl

.config/systemd/user/ndabot.service

```
[Unit]
Description=NDA Discord Bot
After=network.target

[Service]
Type=simple
WorkingDirectory=%h/NDA-Bot
ExecStart=%h/NDA-Bot/venv/bin/python3 -u %h/NDA-Bot/main.py

# Auto-restart if the bot crashes
Restart=always
RestartSec=3

# Unified log file
StandardOutput=append:%h/NDA-Bot/out.log
StandardError=append:%h/NDA-Bot/out.log

[Install]
WantedBy=default.target
```

Ask server owner to run `sudo loginctl enable-linger rizen` so that systemctl works even when my account is logged out.

```
systemctl --user daemon-reexec
systemctl --user daemon-reload
systemctl --user start ndabot.service
systemctl --user enable ndabot.service
```

always `systemctl --user start ndabot.service` after updating main.py
