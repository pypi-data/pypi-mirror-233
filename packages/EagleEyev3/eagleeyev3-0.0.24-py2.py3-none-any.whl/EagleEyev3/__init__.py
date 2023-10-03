""" Python client for Eagle Eye Networks APIv3 """


import json
import logging
import requests

from datetime import datetime, timedelta
from pytz import timezone

from io import BytesIO

logging.basicConfig(level=logging.INFO)

from EagleEyev3._version import __version__
from EagleEyev3.eagleeyev3 import EagleEyev3
from EagleEyev3.device import Device
from EagleEyev3.camera import Camera

