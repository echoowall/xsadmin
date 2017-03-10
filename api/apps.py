from django.apps import AppConfig
import logging
logger = logging.getLogger('xsadminloger')
from django.db.models import Q

class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        logger.info('ApiConfig is ready')
