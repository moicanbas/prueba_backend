import logging
import sqlalchemy
from sqlalchemy import text, insert
from fastapi import FastAPI, BackgroundTasks
import requests
from utils.models import Contact
from dotenv import load_dotenv
import os

load_dotenv()

db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASS")
db_name = os.getenv("DB_NAME")

engine = sqlalchemy.create_engine(
    f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
)

hubspot_access_token = os.getenv("HUBSPOT_ACCESS_TOKEN")
clickup_token = os.getenv("CLICKUP_TOKEN")
list_id = os.getenv("LIST_ID")

# Crear la aplicación FastAPI
app = FastAPI()

@app.post("/contacts")
def create_contact(contact: Contact):
    # Crear el cuerpo de la solicitud con los datos del contacto
    contact_data = {
        "email": contact.email,
        "firstname": contact.firstname,
        "lastname": contact.lastname,
        "phone": contact.phone,
        "website": contact.website
    }

    # Realizar la solicitud POST a la API de HubSpot para crear el contacto
    url = "https://api.hubspot.com/crm/v3/objects/contacts"
    headers = {"Authorization": f"Bearer {hubspot_access_token}", "Content-Type": "application/json"}
    response = requests.post(url, headers=headers, json=contact_data)

    # Verificar el resultado de la operación
    if response.status_code == 201:
        return {"message": "Contacto creado exitosamente"}
    else:
        return {"message": "Error al crear el contacto en HubSpot"}

def sync_contacts_task():
    """Sincronizar contactos entre HubSpot y ClickUp."""
    # Obtener todos los contactos de HubSpot
    url = "https://api.hubapi.com/crm/v3/objects/contacts"
    headers = {"Authorization": f"Bearer {hubspot_access_token}"}
    response = requests.get(url, headers=headers)
    contacts = response.json().get("results", [])

    # Iterar sobre los contactos y crear tareas en ClickUp
    for contact in contacts:
        email = contact.get("properties", {}).get("email")
        if email and not check_task_exists(email):
            title = email
            description = f"{contact['properties']['firstname']} {contact['properties']['lastname']}"
            create_task(title, description)

    # Registrar la llamada en la base de datos
    query = text(f"""
        INSERT INTO api_calls (data, result)
        VALUES ('{contacts}', 'success')
    """)
    with engine.connect() as connection:
        connection.execute(query)

@app.post("/sync-contacts")
def sync_contacts(background_tasks: BackgroundTasks):
    """Iniciar la sincronización de contactos como una tarea en segundo plano."""
    background_tasks.add_task(sync_contacts_task)
    return {"message": "Sincronización de contactos iniciada correctamente"}


def check_task_exists(title):
    url = f"https://api.clickup.com/api/v2/list/{list_id}/task"
    headers = {"Authorization": clickup_token}
    response = requests.get(url, headers=headers)
    tasks = response.json().get("tasks", [])

    for task in tasks:
        if task["name"] == title:
            return True

    return False

def create_task(title, description):
    url = f"https://api.clickup.com/api/v2/list/{list_id}/task"
    headers = {"Authorization": clickup_token}
    payload = {"name": title, "content": description}
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    return None

logging.basicConfig(level=logging.INFO)

# Iniciar la aplicación
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)