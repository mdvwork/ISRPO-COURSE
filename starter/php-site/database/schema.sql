CREATE DATABASE IF NOT EXISTS isrpo_course CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE isrpo_course;

CREATE TABLE users (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(254) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE projects (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL UNIQUE,
    hours SMALLINT UNSIGNED NOT NULL,
    status ENUM('planned', 'active', 'done') NOT NULL DEFAULT 'planned',
    owner_id BIGINT UNSIGNED NULL,
    CONSTRAINT fk_projects_owner FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE SET NULL,
    CONSTRAINT chk_projects_hours CHECK (hours <= 1000)
);

