from enum import Enum

class TripStatus(Enum):
    INACTIVE = 1
    ACTIVE = 2
    FAILED = 3
    SEMI_FAILED = 4
    SUCCESSFUL = 5


class Trip:

    def __init__(self, start_time, end_time, start_id, end_id):
        self.start_time = start_time
        self.end_time = end_time
        if len(start_id) > 0:
            self.start_id = int(start_id)
        else:
            self.start_id = 0
        if len(end_id) > 0:
            self.end_id = int(end_id)
        else:
            self.end_id = 0
        self.status = TripStatus.INACTIVE

    def start_minute_of_day(self):
        return self.start_time.time().minute

    def end_minute_of_day(self):
        return self.end_time.time().minute
