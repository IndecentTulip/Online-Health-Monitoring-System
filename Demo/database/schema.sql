-- Drop the database if it exists
DROP DATABASE IF EXISTS jlabs;

-- Create the database
CREATE DATABASE jlabs WITH ENCODING 'UTF8';

-- Connect to the new database (this part is typically done in the command line or client)
\c jlabs

-- Create users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create posts table
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    user_id INT,
    title VARCHAR(255) NOT NULL,
    content VARCHAR(355) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

