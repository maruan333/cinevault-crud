import os
from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from datetime import datetime

from database import get_database_connection
from repositorios.UsuarioRepository import UsuarioRepository
from repositorios.PeliculaRepository import PeliculaRepository
from repositorios.ActorRepository import ActorRepository
from domain.modelos.Pelicula import PeliculaCreate, PeliculaUpdate


app = FastAPI(title="CineVault CRUD")

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY", "cambia-esto-en-produccion"),
)

base_dir = os.path.dirname(__file__)
app.mount("/static", StaticFiles(directory=os.path.join(base_dir, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(base_dir, "templates"))

usuario_repo = UsuarioRepository()
pelicula_repo = PeliculaRepository()
actor_repo = ActorRepository()


async def get_current_user(request: Request):
    user_id = request.session.get("user_id")
    if not user_id:
        return None

    db = get_database_connection()
    user = usuario_repo.get_by_id(db, user_id)
    db.close()
    return user


async def require_auth(user=Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="No autenticado")
    return user


async def require_admin(user=Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="No autenticado")
    if not user.es_admin:
        raise HTTPException(status_code=403, detail="No autorizado")
    return user


@app.get("/", response_class=HTMLResponse)
async def home(request: Request, user=Depends(get_current_user)):
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    return RedirectResponse(url="/peliculas", status_code=303)


@app.get("/login", response_class=HTMLResponse)
async def login_get(request: Request):
    if request.session.get("user_id"):
        return RedirectResponse(url="/peliculas", status_code=303)
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "error": request.query_params.get("error"),
            "success": request.query_params.get("success"),
        },
    )


@app.post("/login")
async def login_post(request: Request, username: str = Form(...), password: str = Form(...)):
    db = get_database_connection()
    user_data = usuario_repo.get_by_username(db, username)
    db.close()

    if not user_data or not usuario_repo.verificar_password(password, user_data["password_hash"]):
        return RedirectResponse(url="/login?error=Credenciales incorrectas", status_code=303)

    request.session["user_id"] = user_data["id"]
    request.session["username"] = user_data["username"]
    request.session["is_admin"] = bool(user_data["es_admin"])
    return RedirectResponse(url="/peliculas", status_code=303)


@app.get("/register", response_class=HTMLResponse)
async def register_get(request: Request):
    return templates.TemplateResponse(
        "register.html",
        {
            "request": request,
            "error": request.query_params.get("error"),
        },
    )


@app.post("/register")
async def register_post(
    username: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
):
    if password != confirm_password:
        return RedirectResponse(url="/register?error=Las contrasenas no coinciden", status_code=303)

    db = get_database_connection()
    exists = usuario_repo.get_by_username(db, username)
    if exists:
        db.close()
        return RedirectResponse(url="/register?error=Ese usuario ya existe", status_code=303)

    usuario_repo.crear_usuario(db, username=username, password=password, es_admin=False)
    db.close()
    return RedirectResponse(url="/login?success=Registro completado", status_code=303)


@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)


@app.get("/peliculas", response_class=HTMLResponse)
async def peliculas_list(request: Request, buscar: str = None, user=Depends(require_auth)):
    db = get_database_connection()
    peliculas = pelicula_repo.get_all(db, buscar=buscar)
    db.close()
    return templates.TemplateResponse(
        "peliculas_list.html",
        {
            "request": request,
            "peliculas": peliculas,
            "user": user,
            "buscar": buscar or "",
            "success": request.query_params.get("success"),
            "error": request.query_params.get("error"),
        },
    )


@app.get("/peliculas/nueva", response_class=HTMLResponse)
async def peliculas_new_get(request: Request, user=Depends(require_admin)):
    return templates.TemplateResponse(
        "peliculas_form.html",
        {"request": request, "user": user, "pelicula": None, "accion": "crear"},
    )


@app.post("/peliculas/nueva")
async def peliculas_new_post(
    user=Depends(require_admin),
    titulo: str = Form(...),
    anio: int = Form(...),
    director: str = Form(...),
    sinopsis: str = Form(...),
    poster_url: str = Form(""),
):
    payload = PeliculaCreate(
        titulo=titulo,
        anio=anio,
        director=director,
        sinopsis=sinopsis,
        poster_url=poster_url or None,
    )
    db = get_database_connection()
    pelicula_repo.create(db, payload)
    db.close()
    return RedirectResponse(url="/peliculas?success=Pelicula creada", status_code=303)


@app.get("/peliculas/{pelicula_id}/editar", response_class=HTMLResponse)
async def peliculas_edit_get(pelicula_id: int, request: Request, user=Depends(require_admin)):
    db = get_database_connection()
    pelicula = pelicula_repo.get_by_id(db, pelicula_id)
    db.close()
    if not pelicula:
        raise HTTPException(status_code=404, detail="Pelicula no encontrada")

    return templates.TemplateResponse(
        "peliculas_form.html",
        {"request": request, "user": user, "pelicula": pelicula, "accion": "editar"},
    )


@app.post("/peliculas/{pelicula_id}/editar")
async def peliculas_edit_post(
    pelicula_id: int,
    user=Depends(require_admin),
    titulo: str = Form(...),
    anio: int = Form(...),
    director: str = Form(...),
    sinopsis: str = Form(...),
    poster_url: str = Form(""),
):
    payload = PeliculaUpdate(
        titulo=titulo,
        anio=anio,
        director=director,
        sinopsis=sinopsis,
        poster_url=poster_url or None,
    )
    db = get_database_connection()
    pelicula_repo.update(db, pelicula_id, payload)
    db.close()
    return RedirectResponse(url="/peliculas?success=Pelicula actualizada", status_code=303)


@app.post("/peliculas/{pelicula_id}/borrar")
async def peliculas_delete_post(pelicula_id: int, user=Depends(require_admin)):
    db = get_database_connection()
    pelicula_repo.delete(db, pelicula_id)
    db.close()
    return RedirectResponse(url="/peliculas?success=Pelicula eliminada", status_code=303)


@app.get("/actores", response_class=HTMLResponse)
async def actores_list(request: Request, user=Depends(require_auth)):
    db = get_database_connection()
    actores = actor_repo.get_all(db)
    db.close()
    return templates.TemplateResponse(
        "actores_list.html",
        {
            "request": request,
            "actores": actores,
            "user": user,
            "error": request.query_params.get("error"),
            "success": request.query_params.get("success"),
        },
    )


@app.post("/actores/nuevo")
async def actores_new_post(
    user=Depends(require_admin),
    nombre: str = Form(...),
    nacionalidad: str = Form(...),
):
    db = get_database_connection()
    actor_repo.create(db, nombre=nombre, nacionalidad=nacionalidad)
    db.close()
    return RedirectResponse(url="/actores?success=Actor creado", status_code=303)


@app.get("/peliculas/{pelicula_id}/reparto", response_class=HTMLResponse)
async def reparto_get(pelicula_id: int, request: Request, user=Depends(require_auth)):
    db = get_database_connection()
    pelicula = pelicula_repo.get_by_id(db, pelicula_id)
    if not pelicula:
        db.close()
        raise HTTPException(status_code=404, detail="Pelicula no encontrada")

    actores_asignados = pelicula_repo.get_actores_de_pelicula(db, pelicula_id)
    actores_disponibles = pelicula_repo.get_actores_disponibles(db, pelicula_id)
    db.close()
    return templates.TemplateResponse(
        "reparto.html",
        {
            "request": request,
            "user": user,
            "pelicula": pelicula,
            "actores_asignados": actores_asignados,
            "actores_disponibles": actores_disponibles,
            "error": request.query_params.get("error"),
            "success": request.query_params.get("success"),
        },
    )


@app.post("/peliculas/{pelicula_id}/reparto/asignar")
async def reparto_asignar_post(
    pelicula_id: int,
    actor_id: int = Form(...),
    user=Depends(require_admin),
):
    db = get_database_connection()
    pelicula_repo.asignar_actor(db, pelicula_id, actor_id)
    db.close()
    return RedirectResponse(
        url=f"/peliculas/{pelicula_id}/reparto?success=Actor asignado",
        status_code=303,
    )


@app.post("/peliculas/{pelicula_id}/reparto/quitar")
async def reparto_quitar_post(
    pelicula_id: int,
    actor_id: int = Form(...),
    user=Depends(require_admin),
):
    db = get_database_connection()
    pelicula_repo.quitar_actor(db, pelicula_id, actor_id)
    db.close()
    return RedirectResponse(
        url=f"/peliculas/{pelicula_id}/reparto?success=Actor quitado",
        status_code=303,
    )


@app.get("/version")
async def version():
    return {"version": "v0.1.0", "deployed_at": datetime.utcnow().isoformat()}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
