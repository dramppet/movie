CREATE DATABASE movie;
USE movie;

CREATE TABLE roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(20) UNIQUE NOT NULL
);

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role_id INT NOT NULL,
    CONSTRAINT fk_user_role FOREIGN KEY (role_id) REFERENCES roles(id)
);

CREATE TABLE movies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    director VARCHAR(255),
    release_year INT CHECK (release_year > 1888),
    rating DECIMAL(3,1) DEFAULT NULL
);

USE movie;

INSERT INTO roles (name) VALUES ('ADMIN'), ('USER');

INSERT INTO users (username, password_hash, role_id) VALUES 
('admin_ivan', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6L6s57OT67Jm/8m2', 1),
('user_georgi', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6L6s57OT67Jm/8m2', 2); 


INSERT INTO movies (title, director, release_year, rating) VALUES 
('Inception', 'Christopher Nolan', 2010, 8.8),
('The Matrix', 'Lana Wachowski', 1999, 8.7),
('Interstellar', 'Christopher Nolan', 2014, NULL),
('The Godfather', 'Francis Ford Coppola', 1972, 9.2),
('Pulp Fiction', 'Quentin Tarantino', 1994, NULL);
