#!/bin/bash
nginx -t >/dev/null 2>&1
if [ $? -eq 0 ]; then
	/etc/init.d/nginx status > /dev/null 
	if [ $?  -eq "0" ]; then
		/etc/init.d/nginx reload
	else
		echo "Nginx is not running"
	fi
else
    echo "nginx config error"
fi