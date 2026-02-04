CREATE DATABASE IF NOT EXISTS aplicacion;

USE aplicacion;

CREATE TABLE IF NOT EXISTS usuarios(

    id INT AUTO_INCREMENT NOT NULL UNIQUE,
    correo VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    admin VARCHAR(50)


);

CREATE TABLE IF NOT EXISTS favoritos(

    USER_ID Foreign Key (usuarios) REFERENCES (id),
    nombre VARCHAR(150),
    genero VARCHAR(50),
    especie VARCHAR(100),
    imagen VARCHAR(200)


);