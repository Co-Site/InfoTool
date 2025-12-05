ARG BASE_IMAGE_VERSION
FROM geonode/geoserver_data:${BASE_IMAGE_VERSION:-4.4.3}

# configure logging
RUN sed 's|<stdOutLogging>false</stdOutLogging>|<stdOutLogging>true</stdOutLogging>|' -i "/geoserver_data/data/logging.xml"
