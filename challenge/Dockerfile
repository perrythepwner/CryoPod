FROM ghcr.io/foundry-rs/foundry:nightly-c13d42e850da353c0856a8b0d4123e13cc40045d as foundry

FROM blockscout/blockscout:6.9.0 AS blockscout_backend

FROM ghcr.io/blockscout/frontend:v1.36.1 AS blockscout_frontend

FROM hexpm/elixir:1.17.3-erlang-27.1-alpine-3.20.3 as runner

COPY ./backend/requirements.txt /tmp/requirements.txt

RUN apk --no-cache --update add \
    bash \
    python3 \
    py3-pip \
    nodejs \
    curl \
    socat \
    jq \
    unzip \
    git \
    envsubst \
    postgresql15 \
    redis \
    nginx \
    supervisor

RUN python3 -m pip install --break-system-packages --no-cache-dir -r /tmp/requirements.txt && \
    rm -rf /tmp/requirements.txt

RUN addgroup -S blockscout && adduser -S blockscout -G blockscout
RUN addgroup -S ctf && adduser -S ctf -G ctf

COPY ./backend/entrypoint.sh /
COPY ./backend/eth_sandbox/ /usr/lib/python/eth_sandbox/
COPY ./backend/contracts/ /home/ctf/backend/contracts/
COPY ./backend/scripts/ /home/ctf/backend/scripts/

COPY ./config/ /startup/
COPY ./config/nginx.conf /etc/nginx/templates/default.conf.template
COPY ./config/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY ./config/blockscout-db-data /var/lib/postgresql/data/

COPY --from=blockscout_backend /app/ /home/ctf/blockscout_backend/
COPY --from=blockscout_frontend /app/ /home/ctf/blockscout_frontend/

COPY --from=foundry /usr/local/bin/forge /usr/local/bin/forge
COPY --from=foundry /usr/local/bin/cast /usr/local/bin/cast
COPY --from=foundry /usr/local/bin/anvil /usr/local/bin/anvil
COPY --from=foundry /usr/local/bin/chisel /usr/local/bin/chisel

# TODO
#RUN true && \
#    cd /home/ctf/backend/contracts/ && \
#    forge build --out ./compiled && \
#    true

ENV PYTHONPATH=/usr/lib/python/
ENV PYTHONUNBUFFERED=1

RUN chmod +x /entrypoint.sh && \
    mkdir -p /var/log/ctf/ && \
    chown -R ctf:ctf /var/log/ctf/ && \
    chmod 777 /var/log/ctf/ && \
    chown -R ctf:ctf /home/ctf/ && \
    chown -R blockscout:blockscout /home/ctf/blockscout_backend/ && \
    chown -R blockscout:blockscout /home/ctf/blockscout_frontend/ && \
    chmod -R 777 /home/ctf/blockscout_frontend/public && \
    chmod -R 777 /home/ctf/blockscout_frontend/.next && \
    chmod -R 777 /home/ctf/blockscout_frontend/deploy && \
    mkdir -p /run/postgresql/ && \
    chown -R postgres:postgres /run/postgresql/ && \
    chown -R postgres:postgres /var/lib/postgresql/ && \
    su postgres -c "chmod 0700 /var/lib/postgresql/data/"

EXPOSE 80
USER root
WORKDIR /home/ctf/

ENTRYPOINT [ "/entrypoint.sh" ]