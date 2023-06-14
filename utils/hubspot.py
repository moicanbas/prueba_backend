import requests
from dotenv import dotenv_values

config = dotenv_values(".env")
hubspot_access_token = config["HUBSPOT_ACCESS_TOKEN"]

def create_contact_hubspot(contact):
    contact_data = {
        "email": contact.email,
        "firstname": contact.firstname,
        "lastname": contact.lastname,
        "phone": contact.phone,
        "website": contact.website
    }

    url = "https://api.hubspot.com/crm/v3/objects/contacts"
    headers = {"Authorization": f"Bearer {hubspot_access_token}", "Content-Type": "application/json"}
    response = requests.post(url, headers=headers, json=contact_data)

    if response.status_code == 201:
        return {"message": "Contacto creado exitosamente"}
    else:
        return {"message": "Error al crear el contacto en HubSpot"}
