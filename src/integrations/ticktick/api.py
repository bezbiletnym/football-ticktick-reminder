import os

from src.classes.task import Task
from src.integrations.base_api import BaseAPI


class TickTickAPI(BaseAPI):

    _TICKTICK_PROJECT_NAME: str = os.environ.get("TICKTICK_PROJECT_NAME")
    _TICKTICK_BASE_URL: str = 'https://api.ticktick.com/open/v1'


    def _get_headers(self) -> dict:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._TOKEN}",
        }
        return headers


    def get_ticktick_user_project_id(self) -> str:
        print(f"Searching for project {self._TICKTICK_PROJECT_NAME}...")
        url = f"{self._TICKTICK_BASE_URL}/project"
        projects = self._send_request(method='GET', url=url, data={})
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
        response_data = self._send_request(method='POST', url=url, data=data)
        if response_data:
            print("Task created")


    def get_existing_tasks(self, project_id: str) -> list[Task]:
        print(f"Getting tasks from {project_id}...")
        url = f"{self._TICKTICK_BASE_URL}/project/{project_id}/data"
        response_data = self._send_request(method='GET', url=url, data={})
        tasks_dicts_list = response_data.get('tasks', [])
        tasks_list = [Task(title=x.get('title'), content=x.get('content'),
                        due_date=x.get('dueDate')) for x in tasks_dicts_list]
        print(f"Found {len(tasks_list)} existing tasks")
        return tasks_list