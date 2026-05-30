import bcrypt
from domain.modelos.Usuario import Usuario


class UsuarioRepository:
    def get_by_username(self, db, username: str):
        cursor = db.cursor()
        cursor.execute(
            "SELECT id, username, password_hash, es_admin FROM usuarios WHERE username = %s",
            (username,),
        )
        row = cursor.fetchone()
        cursor.close()
        if not row:
            return None
        return {
            "id": row[0],
            "username": row[1],
            "password_hash": row[2],
            "es_admin": bool(row[3]),
        }

    def get_by_id(self, db, user_id: int):
        cursor = db.cursor()
        cursor.execute(
            "SELECT id, username, es_admin FROM usuarios WHERE id = %s",
            (user_id,),
        )
        row = cursor.fetchone()
        cursor.close()
        if not row:
            return None
        return Usuario(id=row[0], username=row[1], es_admin=bool(row[2]))

    def crear_usuario(self, db, username: str, password: str, es_admin: bool = False):
        password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO usuarios (username, password_hash, es_admin) VALUES (%s, %s, %s)",
            (username, password_hash, es_admin),
        )
        db.commit()
        cursor.close()

    def verificar_password(self, plain: str, password_hash):
        if isinstance(password_hash, str):
            password_hash = password_hash.encode("utf-8")
        return bcrypt.checkpw(plain.encode("utf-8"), password_hash)
