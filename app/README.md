# CineVault CRUD

Aplicacion web de peliculas con autenticacion por roles, CRUD y relacion N-M entre peliculas y actores.

## Credenciales iniciales

- Usuario: `admin`
- Contrasena: `admin123`

## Funcionalidades

- Registro, login y logout.
- Roles:
  - Admin: CRUD completo de peliculas, alta de actores y gestion de reparto.
  - Usuario normal: solo lectura.
- Relacion N-M: una pelicula puede tener muchos actores y un actor puede estar en muchas peliculas.
- Busqueda por titulo y director.

## Ejecucion local

```bash
pip install -r requirements.txt
uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

## Base de datos

Ejecuta `init.sql` sobre MySQL.

## Docker compose con Watchtower

```bash
docker compose up -d --build
```

Servicios:
- `db` (MySQL)
- `web` (FastAPI)
- `watchtower` (auto-update de imagenes)

## Pipeline CI/CD

Incluye GitHub Actions en `.github/workflows/ci-cd.yml`.
- CI: instala dependencias y valida sintaxis.
- CD: build y push de imagen si existen secrets.
