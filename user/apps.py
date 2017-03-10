from django.apps import AppConfig
import logging
from .utils import refush_node_app_keyset

logger = logging.getLogger('xsadminloger')

class UserConfig(AppConfig):
    name = 'user'

    def ready(self):
        logger.info('UserConfig is ready')
        refush_node_app_keyset(self.get_model('Node'))

        from . import signals
