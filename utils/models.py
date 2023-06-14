from pydantic import BaseModel

class Contact(BaseModel):
    email: str
    firstname: str
    lastname: str
    phone: str
    website: str
