# Use everytime you need to find out any team's id:
# python -m src.team_search my_team
# Use _ instead of spaces
import sys
import dotenv
dotenv.load_dotenv()

from src.integrations.sport_api.api import SportAPI

team_name = sys.argv[1]

api = SportAPI()
api.search_teams_by_name(team_name)
print("Copy your team's ID to your ENV")