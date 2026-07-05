from dataclasses import dataclass, field
from datetime import datetime, timezone

@dataclass
class Fixture:
    tournament_name: str
    home_team: str
    away_team: str
    start_timestamp: int
    start_string_time: str = field(init=False)
    start_datetime: datetime = field(init=False)

    def _create_datetime_from_timestamp(self):
        dt_object = datetime.fromtimestamp(timestamp=self.start_timestamp, tz=timezone.utc)
        self.start_datetime = dt_object
        self.start_string_time = dt_object.strftime('%Y-%m-%dT%H:%M:%S%z')

    def __post_init__(self):
        self._create_datetime_from_timestamp()