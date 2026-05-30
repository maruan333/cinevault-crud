from domain.modelos.Actor import Actor


class ActorRepository:
    def get_all(self, db):
        cursor = db.cursor()
        cursor.execute("SELECT id, nombre, nacionalidad FROM actores ORDER BY nombre")
        rows = cursor.fetchall()
        cursor.close()
        return [Actor(id=r[0], nombre=r[1], nacionalidad=r[2]) for r in rows]

    def create(self, db, nombre: str, nacionalidad: str):
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO actores (nombre, nacionalidad) VALUES (%s, %s)",
            (nombre, nacionalidad),
        )
        db.commit()
        cursor.close()
