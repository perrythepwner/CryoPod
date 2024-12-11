#!/bin/sh

set -ex

sleep 2 && \
envsubst '${BACK_PROXY_PASS} ${FRONT_PROXY_PASS}' < /etc/nginx/templates/default.conf.template > /etc/nginx/nginx.conf && \
supervisord -c /startup/supervisord.conf -u root && \
tail -f /var/log/ctf/*.log
