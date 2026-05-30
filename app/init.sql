CREATE DATABASE IF NOT EXISTS cinevault;
USE cinevault;

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARBINARY(255) NOT NULL,
    es_admin BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS peliculas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(120) NOT NULL,
    anio INT NOT NULL,
    director VARCHAR(120) NOT NULL,
    sinopsis VARCHAR(600) NOT NULL,
    poster_url VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS actores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL,
    nacionalidad VARCHAR(80) NOT NULL
);

CREATE TABLE IF NOT EXISTS pelicula_actor (
    pelicula_id INT NOT NULL,
    actor_id INT NOT NULL,
    PRIMARY KEY (pelicula_id, actor_id),
    FOREIGN KEY (pelicula_id) REFERENCES peliculas(id) ON DELETE CASCADE,
    FOREIGN KEY (actor_id) REFERENCES actores(id) ON DELETE CASCADE
);

INSERT IGNORE INTO usuarios (id, username, password_hash, es_admin)
VALUES (1, 'admin', 0x243262243132244d314f65652f6d394451626e556e4f62444f6e647965416b4d4943646552456454445143344b2e55447572412e64625071586d344b, TRUE);

INSERT INTO peliculas (titulo, anio, director, sinopsis, poster_url)
SELECT * FROM (
    SELECT 'Blade Runner 2049', 2017, 'Denis Villeneuve', 'Un agente descubre un secreto que puede cambiar el equilibrio social.', 'https://picsum.photos/seed/br2049/320/480'
) AS tmp
WHERE NOT EXISTS (SELECT 1 FROM peliculas WHERE titulo = 'Blade Runner 2049');

INSERT INTO peliculas (titulo, anio, director, sinopsis, poster_url)
SELECT * FROM (
    SELECT 'La Llegada', 2016, 'Denis Villeneuve', 'Una linguista intenta comunicarse con visitantes extraterrestres para evitar un conflicto global.', 'https://picsum.photos/seed/arrival/320/480'
) AS tmp
WHERE NOT EXISTS (SELECT 1 FROM peliculas WHERE titulo = 'La Llegada');

INSERT INTO actores (nombre, nacionalidad)
SELECT * FROM (
    SELECT 'Ryan Gosling', 'Canada'
) AS tmp
WHERE NOT EXISTS (SELECT 1 FROM actores WHERE nombre = 'Ryan Gosling');

INSERT INTO actores (nombre, nacionalidad)
SELECT * FROM (
    SELECT 'Amy Adams', 'Estados Unidos'
) AS tmp
WHERE NOT EXISTS (SELECT 1 FROM actores WHERE nombre = 'Amy Adams');
