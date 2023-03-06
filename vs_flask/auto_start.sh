#!/bin/bash
echo "start jmxs app"
cd /home/vs_flask & python monitor.py &
source go_app.sh 
