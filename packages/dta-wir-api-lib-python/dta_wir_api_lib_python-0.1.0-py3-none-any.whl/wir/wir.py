# coding=utf-8
import json
import logging
from datetime import datetime, timedelta
import re
from warnings import warn
from deprecated import deprecated
from requests import HTTPError

from .errors import ApiNotFoundError, ApiPermissionError
from .models.Sleep import SleepData
from .rest_client import WIRRestAPI
from .utils.sleep import from_promptout_to_sleep_data

log = logging.getLogger(__name__)


class WIR(WIRRestAPI):

    def __init__(self, url, *args, **kwargs):
        if "api_version" not in kwargs:
            kwargs["api_version"] = "v1"

        super(WIR, self).__init__(url, *args, **kwargs)

    def update_diary(self, user_id=0, data=None):
        path = "diaries/users/{}/today".format(user_id)
        full_path = self.url_joiner(self.base_url(), path)

        sleep_data = from_promptout_to_sleep_data(data)

        return self.put(full_path, data=sleep_data.dict())
