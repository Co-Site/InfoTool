#
# Take the GeoNode settings documentation as a reference:
#
# https://docs.geonode.org/en/master/basic/settings/index.html#settings
#

import os
import ast
import sys


# sets defaults settings and from .env
from geonode.settings import *  # noqa
from geonode.settings import (  # noqa
    DEBUG,
    INSTALLED_APPS,
    SITEURL,
    TEMPLATES,
)
from geonode.services.enumerations import HARVESTER_TYPES

X_FRAME_OPTIONS = "SAMEORIGIN"
SECURE_CROSS_ORIGIN_OPENER_POLICY = None if DEBUG else "same-origin"


# relax origins for geonode-mapstore-client development
CSRF_TRUSTED_ORIGINS = (
    [
        "http://localhost",
        "http://localhost:8081",
        "http://localhost:8001",
    ]
    if DEBUG
    else ast.literal_eval(os.getenv("CSRF_TRUSTED_ORIGINS", "[]"))
)  # noqa
CORS_ALLOWED_ORIGINS = (
    [
        "http://localhost",
        "http://localhost:8081",
        "http://localhost:8001",
    ]
    if DEBUG
    else ast.literal_eval(os.getenv("CORS_ALLOWED_ORIGINS", "[]"))
)  # noqa
CORS_ALLOWED_ORIGIN_REGEXES = (
    [
        # match localhost with any port
        r"^http:\/\/localhost:*([0-9]+)?$",
        r"^https:\/\/localhost:*([0-9]+)?$",
    ]
    if DEBUG
    else ast.literal_eval(os.getenv("CORS_ALLOWED_ORIGIN_REGEXES", "[]"))
)  # noqa


STATIC_ROOT = "/mnt/volumes/statics/static/"
MEDIA_ROOT = "/mnt/volumes/statics/uploaded/"
ASSETS_ROOT = "/mnt/volumes/statics/assets/"


# Defines the directory that contains the settings file as the LOCAL_ROOT
# It is used for relative settings elsewhere.
LOCAL_ROOT = os.path.abspath(os.path.dirname(__file__))


# Additional directories which hold static files
# - Give priority to local ones
TEMPLATES[0]["DIRS"].insert(0, "/usr/src/geonode/templates")
loaders = [
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
]
TEMPLATES[0]["OPTIONS"]["loaders"] = loaders
TEMPLATES[0].pop("APP_DIRS", None)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",  # noqa
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},  # noqa
    "handlers": {
        "console": {
            #"level": "WARNING", # no global level
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "simple",
        },
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    "loggers": {
        "root": {
            "handlers": ["console"],
            "level": "WARNING",
        },
        "django": {
            "level": "INFO",
        },
        "geonode": {
            "level": "INFO",
        },
        "geoserver-restconfig.catalog": {
            "level": "ERROR",
        },
        "owslib": {
            "level": "ERROR",
        },
        "pycsw": {
            "level": "ERROR",
        },
        "celery": {
            "level": "INFO",
        },
        "mapstore2_adapter.plugins.serializers": {
            "level": "INFO",
        },
        "geonode_logstash.logstash": {
            "level": "INFO",
        },
        "geonode_sta": {
            "level": "DEBUG",
        }
    },
}

INSTALLED_APPS += (
    "geonode_sta",
    "externalapplications",
    "customizations",
    "subsites",
)

# SUBSITE SPECIFIC CONFIGURATION
ENABLE_SUBSITE_CUSTOM_THEMES = True
ENABLE_CATALOG_HOME_REDIRECTS_TO = False
# return download_resourcebase and view resourcebase as permissions
SUBSITE_READ_ONLY = False
# If TRUE will hide the `subsite_exclusive` resources also from the detailed endpoint `/documents`, `/maps`, `/datasets`, '/geoapps`
SUBSITE_HIDE_EXCLUSIVE_FROM_SPECIFIC_API = True

#
#   STA specific settings
#
harvester_class = 'geonode_sta.harvester.Worker'
HARVESTER_CLASSES = [harvester_class]
HARVESTER_TYPES["STA"] = harvester_class

if 'SERVICES_TYPE_MODULES' not in locals():
    SERVICES_TYPE_MODULES = []

if 'geonode_sta.service.Registry' not in SERVICES_TYPE_MODULES:
    SERVICES_TYPE_MODULES.append('geonode_sta.service.Registry')


ROOT_URLCONF = 'geonode_sta.urls'

#
#   Fix SSL behind app-proxy
#
if SITEURL.startswith("https"):
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
