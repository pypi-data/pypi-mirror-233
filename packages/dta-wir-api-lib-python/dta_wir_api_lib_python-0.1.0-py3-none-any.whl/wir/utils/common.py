import json
import ast
from datetime import datetime

from wir.models.Sleep import SleepData



def typecast_bool(value: str):
    return value.lower() == "true"