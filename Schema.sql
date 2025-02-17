CREATE DATABASE IF NOT EXISTS contactmdb;
USE contactmdb;

CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(45) NOT NULL,
    PRIMARY KEY (email)
);

CREATE TABLE IF NOT EXISTS contacts (
    id INT AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    contact VARCHAR(255) NOT NULL,
    city VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);