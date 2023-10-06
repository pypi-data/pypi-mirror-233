import json
from datetime import datetime
from dateutil.parser import parse


from wir.models.Sleep import SleepData, AnswerData
from wir.utils.common import typecast_bool



def from_promptout_to_sleep_data(promptout_data):
    start_time = datetime.fromisoformat(promptout_data["start_time"])
    lot = int(start_time.timestamp())

    bok = promptout_data["time_to_fall_asleep"]["time"]
    ast = lot + (int(bok) * 60)

    dns = typecast_bool(promptout_data["did_not_sleep"])

    wake_up_time = parse(promptout_data["wake_up_time"])
    aet = int(wake_up_time.timestamp())
    date = wake_up_time.replace(hour=0, minute=0, second=0, microsecond=0)

    answer = AnswerData(
        lot=lot,
        ast=ast,
        aet=aet,
        dns=dns,
        nap=int(promptout_data["nap"]["time"]),
        sleepQuality=int(promptout_data["sleep_quality"]),
        tst=300, #Fixme hardcode
    )

    sleep_data = SleepData(
        answer=answer,
        date=int(date.timestamp())
    )

    return sleep_data
