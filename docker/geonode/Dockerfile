# set ARG here globally
ARG BASE_IMAGE_VERSION

# --- Stage 1: Build from Submodule ---
FROM node:20-slim AS builder
RUN corepack enable && corepack prepare pnpm@10.18.3 --activate

WORKDIR /app
COPY ./opt-sta-client .

ENV CI=true

RUN pnpm install --frozen-lockfile
RUN pnpm run build

# --- Stage 2: Build runstage  ---
FROM geonode/geonode:${BASE_IMAGE_VERSION:-4.4.3}

COPY ./requirements.txt /usr/src/more_requirements.txt
RUN yes w | pip install --src /usr/src -r /usr/src/more_requirements.txt

RUN true \
    # django logs are written to stdout by default (see uwsgi.ini)
    # forward celery logs to docker log collector
    && ln -sf /dev/stdout ${CELERY__LOG_FILE:-/var/log/celery.log}


#cp from stage1 builder
COPY --from=builder /app/dist/www /usr/src/geonode/geonode/static/lib/js/
#RUN rm .env*
