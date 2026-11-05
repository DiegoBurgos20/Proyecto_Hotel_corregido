# Hotel Aurora – versión revisada

## Requisitos
- Python 3.10 o superior
- MySQL Server y una base de datos llamada `hotel_db`
- Dependencias de `requirements.txt`

## Instalación en Windows (CMD)
Desde la carpeta `Proyecto_Hotel` (donde está `manage.py`):

```bat
py -m venv venv
venv\Scripts\activate
py -m pip install -r requirements.txt
```

Copia `.env.example` como `.env` y ajusta `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST` y `DB_PORT`. Si usas XAMPP con root sin contraseña, `DB_PASSWORD` puede quedar vacío.

```bat
py manage.py check
py manage.py makemigrations habitaciones
py manage.py migrate
py manage.py createsuperuser
py manage.py test habitaciones
py manage.py runserver
```

Abre `http://127.0.0.1:8000/` e inicia sesión en `/ingreso/`.

## API REST y token
1. Solicita token con `POST /api/token/` y JSON:
   `{"username":"tu_usuario","password":"tu_contraseña"}`
2. Envía el token en las solicitudes protegidas usando el encabezado:
   `Authorization: Token TU_TOKEN`

Endpoints:
- `GET /api/habitaciones/` listar
- `POST /api/habitaciones/` crear
- `GET /api/habitaciones/<id>/` consultar
- `PUT /api/habitaciones/<id>/` actualizar
- `DELETE /api/habitaciones/<id>/` eliminar
- `POST /api/logout/` invalidar token

Todos los endpoints de habitaciones requieren token. Los datos se envían y reciben como JSON. Los códigos habituales son 200, 201, 204, 400, 401 y 404.

## Importante sobre MySQL
Django no crea la base de datos MySQL automáticamente. Crea primero `hotel_db` desde MySQL Workbench o phpMyAdmin. Luego ejecuta `makemigrations` y `migrate`. La persistencia real depende de que MySQL esté iniciado y que las credenciales sean correctas.

## Git
Esta carpeta es una copia de trabajo. No incluye el historial `.git` ni el entorno virtual del ZIP original. Para subirla, copia los cambios a tu clon del repositorio y realiza commits en tu rama de trabajo. No se hizo push ni merge automáticamente.
