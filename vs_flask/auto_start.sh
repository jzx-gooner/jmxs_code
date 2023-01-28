#!/bin/bash
echo "start apache2"
/etc/init.d/apache2 start
echo "start jmxs app"
python /home/vs_flask/app.py
