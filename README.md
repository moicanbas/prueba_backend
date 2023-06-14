# prueba_backend
Prueba Tecnica puesto desarrollador backend python

# API de Sincronización de Contactos

Esta es una API REST en Python utilizando FastAPI que te permite crear contactos en HubSpot y sincronizarlos con ClickUp. Al mismo tiempo, registra cada llamada a la API en una base de datos PostgreSQL.

## Requisitos

- Docker
- Cuenta de HubSpot
- Cuenta de ClickUp

## Configuración

1. Clona el repositorio:

```bash
git clone https://github.com/moicanbas/prueba_backend.git
```

2. Ve al directorio del proyecto:
```bash
cd prueba_backend
```
3. Crea un archivo .env en el directorio raíz del proyecto con la siguiente configuración:  
    La envio por correo

## USO
1. Construye la imagen de Docker:  
```bash
docker build -t nombre_imagen .
```

2. Ejecuta el contenedor de Docker:
```bash
docker run -p 8000:8000 --env-file .env nombre_imagen
```

3. La API estará disponible en http://localhost:8000

4. Para crear un nuevo contacto en HubSpot, realiza una solicitud POST a http://localhost:8000/contacts con los siguientes datos en el cuerpo de la solicitud:
{
    "email": "test@orbidi.com",
    "firstname": "Test",
    "lastname": "Orbidi",
    "phone": "(322) 123-4567",
    "website": "orbidi.com"
}

5. Para sincronizar los contactos entre HubSpot y ClickUp, realiza una solicitud POST a http://localhost:8000/sync-contacts. Este proceso se ejecutará en segundo plano y agregará los contactos creados en HubSpot como tareas en la lista especificada en ClickUp.




