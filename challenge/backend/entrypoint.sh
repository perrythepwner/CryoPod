#!/bin/sh

set -ex

envsubst '${BACK_PROXY_PASS} ${FRONT_PROXY_PASS}' < /etc/nginx/templates/default.conf.template > /etc/nginx/nginx.conf && \
touch /var/log/ctf/${ANVIL_LOGFILE} && \
chown ctf:ctf /var/log/ctf/${ANVIL_LOGFILE} && \
supervisord -c /startup/supervisord.conf -u root && \
tail -f /var/log/ctf/*.log
