import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'Nenniltoz.settings'

import django

django.setup()

import logging

from Collection.models import QuickResult

logger = logging.getLogger("logger")


def update_oracles_results(param):
    logger.info("Param: " + param)
    QuickResult.run_oracles()