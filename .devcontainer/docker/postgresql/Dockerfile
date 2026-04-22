ARG BASE_IMAGE_VERSION
FROM geonode/postgis:${BASE_IMAGE_VERSION:-15.3-latest}

COPY ./prepare-testdb.sh /docker-entrypoint-initdb.d/prepare-testdb.sh
RUN chmod +x /docker-entrypoint-initdb.d/prepare-testdb.sh
