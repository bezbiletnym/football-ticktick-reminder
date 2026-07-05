import os

from datetime import datetime, timedelta, timezone
import dotenv
dotenv.load_dotenv()

from src.classes.task import Task
from src.classes.fixture import Fixture
from src.integrations.ticktick.api import TickTickAPI
from src.integrations.sport_api.api import SportAPI


def fixture_to_task(fixture: Fixture) -> Task:
    return Task(title = f"{fixture.home_team} — {fixture.away_team}",
                content = f"{fixture.tournament_name}:\n"
                f"{fixture.home_team} — {fixture.away_team}",
                due_date = fixture.start_string_time,)


def is_within_next_n_weeks(target_datetime: datetime, n: int):
    now = datetime.now(timezone.utc)
    n_weeks_from_now = now + timedelta(weeks=n)
    return now <= target_datetime <= n_weeks_from_now


def run():
    events = []
    for team_id in MY_TEAMS_IDS:
        events.extend(sport_api.get_team_next_events(team_id=int(team_id)))

    if not events:
        print(f"No next events found for {MY_TEAMS_IDS}")
        return

    project_id = ticktick_api.get_ticktick_user_project_id()
    existing_tasks = ticktick_api.get_existing_tasks(project_id=project_id)

    print(f"Filtering new events which are in the next {NEXT_WEEKS_NUMBER} weeks...")
    for event in events:
        tournament_name = event['season']['name']  # Basically, it's tournament name + year
        home_team = event['homeTeam']['name']
        away_team = event['awayTeam']['name']
        start_timestamp = event['startTimestamp']
        fixture = Fixture(tournament_name=tournament_name, home_team=home_team, away_team=away_team,
                          start_timestamp=start_timestamp)
        if is_within_next_n_weeks(target_datetime=fixture.start_datetime, n=NEXT_WEEKS_NUMBER):
            task = fixture_to_task(fixture=fixture)
            if task not in existing_tasks:
                ticktick_api.create_ticktick_task(project_id=project_id, task=task)
            else:
                print(f"{task.title} task already exists")


print("Starting the job...")
ticktick_api = TickTickAPI()
sport_api = SportAPI()
MY_TEAMS_IDS = str(os.environ.get("MY_TEAMS_IDS")).split(',')
NEXT_WEEKS_NUMBER = int(os.environ.get("NEXT_WEEKS_NUMBER", 4))
# Matches that are closer in time are less likely to be postponed, so defaulting 4
run()
print("The job is completed!")





