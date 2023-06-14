import requests
from dotenv import dotenv_values

config = dotenv_values(".env")
clickup_token = config["CLICKUP_TOKEN"]
list_id = config["CLICKUP_LIST_ID"]

def sync_contacts_clickup(contacts):
    url = f"https://api.clickup.com/api/v2/list/{list_id}/task"
    headers = {"Authorization": clickup_token}

    for contact in contacts:
        email = contact.get("properties", {}).get("email")
        if email and not check_task_exists(email):
            title = email
            description = f"{contact['properties']['firstname']} {contact['properties']['lastname']}"
            create_task_clickup(title, description)

def check_task_exists(title):
    url = f"https://api.clickup.com/api/v2/list/{list_id}/task"
    headers = {"Authorization": clickup_token}
    response = requests.get(url, headers=headers)
    tasks = response.json().get("tasks", [])

    for task in tasks:
        if task["name"] == title:
            return True

    return False

def create_task_clickup(title, description):
    url = f"https://api.clickup.com/api/v2/list/{list_id}/task"
    headers = {"Authorization": clickup_token}
    payload = {"name": title, "content": description}
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    return None
