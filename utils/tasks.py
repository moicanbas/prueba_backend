from hubspot import sync_contacts_hubspot
from clickup import sync_contacts_clickup

def sync_contacts_task():
    contacts = sync_contacts_hubspot()
    sync_contacts_clickup(contacts)
