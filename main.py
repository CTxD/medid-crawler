import logging
import json

from source import config


logger = logging.getLogger('source')

logger.info(f'from main, with name: {__name__}')
config.readconfig('config.cfg')

print(json.dumps(config.CONFIG, indent=4))