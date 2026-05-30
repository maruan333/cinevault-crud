# CineVault CRUD

Aplicacion web de peliculas hecha con FastAPI, Jinja2 y MySQL.

## Que incluye

- Login, logout y registro de usuarios.
- Roles: admin y usuario normal.
- CRUD de peliculas.
- Relacion N-M entre peliculas y actores.
- Busqueda en el listado.
- Docker, Watchtower y GitHub Actions.

## Credenciales por defecto

- Usuario: `admin`
- Contrasena: `admin123`

## Ejecucion local

```bash
cd app
python -m pip install -r requirements.txt
uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

## Docker

```bash
docker compose up -d --build
docker compose ps
```

## GitHub Actions

El workflow esta en `.github/workflows/ci-cd.yml`.

- CI: instala dependencias y valida sintaxis.
- CD: construye la imagen Docker y la publica en Docker Hub si configuras los secrets.

## Secrets necesarios en GitHub

- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN`

## Base de datos para DBeaver

- Host: `localhost`
- Puerto: `3307`
- Usuario: `cinevault`
- Contrasena: `cinevault123`
- Base de datos: `cinevault`

## Estructura

- `app/` -> codigo, templates y estilos.
- `docker-compose.yml` -> servicios de app, MySQL y Watchtower.
- `.github/workflows/ci-cd.yml` -> pipeline de CI/CD.