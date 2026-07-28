# set ARG here globally
ARG BASE_IMAGE_VERSION=4.4.3

# --- Stage 1: Build opt-sta-client ---
FROM node:20-slim AS opt-sta-builder
RUN corepack enable && corepack prepare pnpm@10.18.3 --activate

WORKDIR /app
COPY ./opt-sta-client .

ENV CI=true

RUN pnpm install --frozen-lockfile
RUN pnpm run build


# --- Stage 2: Build MapStore-Client ---
FROM node:20-slim AS mapstore-builder
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY ./gn-mapstore-client .
RUN find . -name ".git" -exec rm -rf {} +

WORKDIR /app/geonode_mapstore_client/client
RUN npm install && npm run compile


# --- Stage 3: Build runstage  ---
FROM geonode/geonode:${BASE_IMAGE_VERSION}

COPY ./requirements.txt /usr/src/more_requirements.txt
RUN yes w | pip install --src /usr/src -r /usr/src/more_requirements.txt

RUN true \
    # django logs are written to stdout by default (see uwsgi.ini)
    # forward celery logs to docker log collector
    && ln -sf /dev/stdout ${CELERY__LOG_FILE:-/var/log/celery.log}

# Copy and install the compiled MapStore client
COPY --from=mapstore-builder /app /usr/src/gn-mapstore-client
RUN pip install /usr/src/gn-mapstore-client

# Copy opt-sta-client
COPY --from=opt-sta-builder /app/dist/www /usr/src/geonode/geonode/static/lib/js/
#RUN rm .env*
