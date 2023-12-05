#!/bin/sh

set -e

# environment subsitute
# replace any environment variables calls in conf.tpl and output it into default.conf NGINX
envsubst < /etc/nginx/default.conf.tpl > /etc/nginx/conf.d/default.conf
# starts nginx with default.conf in the foreground - all logs would be outputted on the screen into docker
nginx -g 'daemon off;'