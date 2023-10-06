import datetime
from pydantic import BaseModel
import requests
import os
import logging
from typing import Optional
import argparse
from dateutil.parser import parse

logging.basicConfig(level=logging.INFO, format="%(filename)s: %(message)s")
log = logging.getLogger()


def empty_to_none(v: str) -> Optional[str]:
    if v == "":
        return None
    return v


### Models
class Slot(BaseModel):

    date: datetime.date


class Response(BaseModel):
    slots: list[Slot]


class Assignment(BaseModel):
    slot: Slot


# todo - it appears mybxl is transitioning to a new API.
# Below one still works, but might need adjustments
def retrieve_slots():
    BRUCITY_APPOINTMENTS_LINK = "https://webcalendar.brucity.be/qmaticwebbooking/rest/schedule/branches/e58833ee8321437b292cd75df53f283fdc0b56ca09b678971ad3ca509edcb862/dates;servicePublicId=hide4bdeed5e052e227a8d0179af81d7f3d9199a6c2fa5a9d7138bca96fb;customSlotLength=35"
    response = Response(slots=requests.get(BRUCITY_APPOINTMENTS_LINK).json())
    return response.slots


def process_appointment(new_date: datetime.date, old_date: datetime.date) -> None:
    if new_date < old_date:
        notify("New slot available", new_date)
        log.info(f"Found. Current: {old_date}, closest found: {new_date}")
    else:
        log.info(f"No sooner slots found. Current: {old_date}, closest: {new_date}")


def notify(title, text):
    os.system(f'osascript -e \'display notification "{text}!" with title "{title}"\'')


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("old_date")

    args = parser.parse_args()
    old_date = parse(args.old_date)

    available_slots = retrieve_slots()

    if available_slots:
        latest_slot = available_slots[0]
        process_appointment(latest_slot.date, old_date.date())


if __name__ == "__main__":
    run()
