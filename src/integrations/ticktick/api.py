import os
import requests

from src.classes.task import Task

class TickTickAPI:

    _TICKTICK_API_TOKEN = os.environ.get("TICKTICK_API_TOKEN")
    _TICKTICK_PROJECT_NAME = os.environ.get("TICKTICK_PROJECT_NAME")
    _TICKTICK_BASE_URL='https://api.ticktick.com/open/v1'


    def _get_headers(self) -> dict:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._TICKTICK_API_TOKEN}",
        }
        return headers


    def get_ticktick_user_project_id(self) -> str:
        print(f"Searching for project {self._TICKTICK_PROJECT_NAME}...")
        url = f"{self._TICKTICK_BASE_URL}/project"
        try:
            response = requests.get(url, headers=self._get_headers())
            response.raise_for_status()
            projects = response.json()
        except Exception as e:
            print(f"Something went wrong: {repr(e)}")
            return ''
        for project in projects:
            if project.get('name') == self._TICKTICK_PROJECT_NAME:
                project_id = project.get('id')
                print(f"Project id is {project_id}")
                return project_id
        return ''


    def create_ticktick_task(self, project_id: str, task: Task):
        print(f"Creating a new task ({task.title}) at {project_id}...")
        url = f"{self._TICKTICK_BASE_URL}/task"
        data = {
            "title": task.title,
            "projectId": project_id,
            "content": task.content,
            "dueDate": task.due_date,
            "reminders": ["TRIGGER:PT0S"]
        }
        try:
            response = requests.post(url, headers=self._get_headers(), json=data)
            response.raise_for_status()
            print("Task created")
        except Exception as e:
            print(f"Something went wrong: {repr(e)}")

    def get_existing_tasks(self, project_id: str) -> list[Task]:
        print(f"Getting tasks from {project_id}...")
        url = f"{self._TICKTICK_BASE_URL}/project/{project_id}/data"
        try:
            response = requests.get(url, headers=self._get_headers())
            response.raise_for_status()
            tasks_dicts_list = response.json().get('tasks', [])
            tasks_list = [Task(title=x.get('title'), content=x.get('content'),
                            due_date=x.get('dueDate')) for x in tasks_dicts_list]
            print(f"Found {len(tasks_list)} existing tasks")
            return tasks_list
        except Exception as e:
            print(f"Something went wrong: {repr(e)}")
        return []