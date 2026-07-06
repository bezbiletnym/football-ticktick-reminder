from src.integrations.base_api import BaseAPI


class SportAPI(BaseAPI):

    _SPORT_API_BASE_URL: str = "https://sportapi7.p.rapidapi.com/api/v1"

    def _get_headers(self) -> dict:
        headers = {
            "x-rapidapi-key": self._TOKEN,
            "x-rapidapi-host": "sportapi7.p.rapidapi.com",
            "Content-Type": "application/json"
        }
        return headers


    def get_team_next_events(self, team_id: int) -> list:
        print(f"Getting next events for {team_id}...")
        url = f"{self._SPORT_API_BASE_URL}/team/{team_id}/events/next/0"
        response_data = self._send_request(method="GET", url=url, data={})
        events = response_data.get('events', [])
        print(f"Found {len(events)} events for {team_id}")
        return events


    def search_teams_by_name(self, team_name: str):
        print(f"Searching for {team_name}...")
        url = f"{self._SPORT_API_BASE_URL}/search/teams/{team_name}/more"
        response_data = self._send_request(method="GET", url=url, data={})
        teams = response_data.get('teams', [])
        if teams:
            print(f"Found {len(teams)} teams")
        for team in teams:
            if team.get('sport', {}).get('slug') == 'football':
                print(f"{team.get('id')}: {team.get('name')}, "
                      f"({team.get('gender')}), "
                      f"{team.get('country', {}).get('name')}")
