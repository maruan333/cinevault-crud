from domain.modelos.Pelicula import Pelicula
from domain.modelos.Actor import Actor


class PeliculaRepository:
    def get_all(self, db, buscar: str | None = None):
        cursor = db.cursor()
        if buscar:
            query = """
                SELECT id, titulo, anio, director, sinopsis, poster_url
                FROM peliculas
                WHERE LOWER(titulo) LIKE %s OR LOWER(director) LIKE %s
                ORDER BY anio DESC, titulo
            """
            pattern = f"%{buscar.lower()}%"
            cursor.execute(query, (pattern, pattern))
        else:
            cursor.execute(
                "SELECT id, titulo, anio, director, sinopsis, poster_url FROM peliculas ORDER BY anio DESC, titulo"
            )

        rows = cursor.fetchall()
        cursor.close()
        return [
            Pelicula(
                id=r[0],
                titulo=r[1],
                anio=r[2],
                director=r[3],
                sinopsis=r[4],
                poster_url=r[5],
            )
            for r in rows
        ]

    def get_by_id(self, db, pelicula_id: int):
        cursor = db.cursor()
        cursor.execute(
            "SELECT id, titulo, anio, director, sinopsis, poster_url FROM peliculas WHERE id = %s",
            (pelicula_id,),
        )
        row = cursor.fetchone()
        cursor.close()
        if not row:
            return None
        return Pelicula(
            id=row[0],
            titulo=row[1],
            anio=row[2],
            director=row[3],
            sinopsis=row[4],
            poster_url=row[5],
        )

    def create(self, db, pelicula):
        cursor = db.cursor()
        cursor.execute(
            """
            INSERT INTO peliculas (titulo, anio, director, sinopsis, poster_url)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                pelicula.titulo,
                pelicula.anio,
                pelicula.director,
                pelicula.sinopsis,
                pelicula.poster_url,
            ),
        )
        db.commit()
        cursor.close()

    def update(self, db, pelicula_id: int, pelicula):
        cursor = db.cursor()
        cursor.execute(
            """
            UPDATE peliculas
            SET titulo = %s, anio = %s, director = %s, sinopsis = %s, poster_url = %s
            WHERE id = %s
            """,
            (
                pelicula.titulo,
                pelicula.anio,
                pelicula.director,
                pelicula.sinopsis,
                pelicula.poster_url,
                pelicula_id,
            ),
        )
        db.commit()
        cursor.close()

    def delete(self, db, pelicula_id: int):
        cursor = db.cursor()
        cursor.execute("DELETE FROM peliculas WHERE id = %s", (pelicula_id,))
        db.commit()
        cursor.close()

    def get_actores_de_pelicula(self, db, pelicula_id: int):
        cursor = db.cursor()
        cursor.execute(
            """
            SELECT a.id, a.nombre, a.nacionalidad
            FROM pelicula_actor pa
            JOIN actores a ON a.id = pa.actor_id
            WHERE pa.pelicula_id = %s
            ORDER BY a.nombre
            """,
            (pelicula_id,),
        )
        rows = cursor.fetchall()
        cursor.close()
        return [Actor(id=r[0], nombre=r[1], nacionalidad=r[2]) for r in rows]

    def get_actores_disponibles(self, db, pelicula_id: int):
        cursor = db.cursor()
        cursor.execute(
            """
            SELECT id, nombre, nacionalidad
            FROM actores
            WHERE id NOT IN (
                SELECT actor_id FROM pelicula_actor WHERE pelicula_id = %s
            )
            ORDER BY nombre
            """,
            (pelicula_id,),
        )
        rows = cursor.fetchall()
        cursor.close()
        return [Actor(id=r[0], nombre=r[1], nacionalidad=r[2]) for r in rows]

    def asignar_actor(self, db, pelicula_id: int, actor_id: int):
        cursor = db.cursor()
        cursor.execute(
            "INSERT IGNORE INTO pelicula_actor (pelicula_id, actor_id) VALUES (%s, %s)",
            (pelicula_id, actor_id),
        )
        db.commit()
        cursor.close()

    def quitar_actor(self, db, pelicula_id: int, actor_id: int):
        cursor = db.cursor()
        cursor.execute(
            "DELETE FROM pelicula_actor WHERE pelicula_id = %s AND actor_id = %s",
            (pelicula_id, actor_id),
        )
        db.commit()
        cursor.close()
