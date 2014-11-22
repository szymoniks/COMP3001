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
        self.start_id = start_id
        self.end_id = end_id
        self.status = TripStatus.INACTIVE
