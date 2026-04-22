ARG BASE_IMAGE_VERSION
FROM postgis/postgis:${BASE_IMAGE_VERSION:-18-3.6-alpine}

# Install jq for JSON processing
RUN apk add --no-cache jq

COPY entrypoint-wrapper.sh /usr/local/bin/entrypoint-wrapper.sh
RUN chmod +x /usr/local/bin/entrypoint-wrapper.sh

COPY *schema*.sh /docker-entrypoint-initdb.d/

ENTRYPOINT ["/usr/local/bin/entrypoint-wrapper.sh"]
