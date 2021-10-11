#!/bin/bash
exec /usr/local/bin/python3.9 fetch_alerts.py &
exec /usr/local/bin/python3.9 launch_scrapping.py