# Football TickTick Reminder

Cronjob to find your favourite teams' next matches and send reminders to your TickTick account.

Uses [SportAPI (Free tier)](https://rapidapi.com/rapidsportapi/api/sportapi7).

## Starting:
1. Rename *.env.example* to *.env*
2. Subscribe to [SportAPI](https://rapidapi.com/rapidsportapi/api/sportapi7) (the free tier gives you 50 requests per month) and copy your x-rapidapi-key to *.env* (X_RAPIDAPI_KEY)
3. Copy your [TickTick API token](#where-to-get-ticktick-api-token) to your *.env* (TICKTICK_API_TOKEN)
4. Create a List in TickTick for your football reminders and copy its name to *.env* (TICKTICK_PROJECT_NAME). **Note** that if you give an icon to your list, you need to copy that too (e.g. `'⚽Football Reminders'`) 
5. [Search for your teams' IDs](#how-to-find-out-your-teams-ids) and copy them to your *.env*, separated with commas (e.g. `MY_TEAMS_IDS=2526,24264`)
6. Schedule `python -m src.cronjob` on your server.

**Optional**: You can change NEXT_WEEKS_NUMBER in *.env*. If a match that the script has found is the next {NEXT_WEEKS_NUMBER} weeks, it will be added to your reminders. I default this value as 4 to not overwhelm my reminders list and to get the most actual teams' schedules.


### Where to get TickTick API token:
Log in to the TickTick web app, click your avatar in the top-left corner, and go to Settings > Account > API Token to create and copy a token
[(source)](https://help.ticktick.com/articles/7465251130025443328).


### How to find out your teams' IDs:
Run this in your CLI:

`python -m src.team_search my_team`
(use _ instead of spaces)

You will get a list of teams like this:
````
2526: FC St. Pauli, (M), Germany
5800: FC St Pauli II U23, (M), Germany
52878: St. Pauli U19, (M), Germany
484509: FC St Pauli, (F), None
1099102: FC St Pauli, (F), Germany
520583: FC St. Pauli III, (None), Germany
1103533: Republic of St. Pauli, (M), Germany
1242207: FC St. Pauli IV, (M), Germany
````
Find your team's ID and copy it to your *.env*. (e.g. `MY_TEAMS_IDS=2526,24264` for FC St. Pauli and Girona FC)
