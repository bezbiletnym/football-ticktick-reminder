import os
import requests

class SportAPI:

    _X_RAPIDAPI_KEY = os.environ.get("X_RAPIDAPI_KEY")


    def _get_headers(self) -> dict:
        headers = {
            "x-rapidapi-key": self._X_RAPIDAPI_KEY,
            "x-rapidapi-host": "sportapi7.p.rapidapi.com",
            "Content-Type": "application/json"
        }
        return headers


    def get_team_next_events(self, team_id: int) -> list:
        print(f"Getting next events for {team_id}...")
        url = f"https://sportapi7.p.rapidapi.com/api/v1/team/{team_id}/events/next/0"
        try:
            response = requests.get(url, headers=self._get_headers())
            response.raise_for_status()
            events = response.json().get('events', [])
            print(f"Found {len(events)} events for {team_id}")
            return events
        except Exception as e:
            print(f"Something went wrong: {repr(e)}")
        return []


    def search_teams_by_name(self, team_name: str):
        print(f"Searching for {team_name}...")
        teams = []
        url = f"https://sportapi7.p.rapidapi.com/api/v1/search/teams/{team_name}/more"
        try:
            response = requests.get(url, headers=self._get_headers())
            response.raise_for_status()
            teams = response.json().get('teams', [])
        except Exception as e:
            print(f"Something went wrong: {repr(e)}")
        if teams:
            print(f"Found {len(teams)} teams")
        for team in teams:
            if team.get('sport', {}).get('slug') == 'football':
                print(f"{team.get('id')}: {team.get('name')}, "
                      f"({team.get('gender')}), "
                      f"{team.get('country', {}).get('name')}")
