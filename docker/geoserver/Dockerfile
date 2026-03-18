ARG BASE_IMAGE_VERSION=2.24.4-latest
FROM geonode/geoserver:${BASE_IMAGE_VERSION}

## GeoServer plugins
#
# Make sure GeoServer container is prepared for each plugin!
# Use further RUN statements to install necessary dependencies.
# Refer to plugin documentation what is required to use a plugin.
COPY ./plugins /usr/local/tomcat/webapps/geoserver/WEB-INF/lib
