-- Mental Wellness & Mood Tracking DBMS Project
-- Run this once in MySQL Workbench / mysql CLI to set up the database.

CREATE DATABASE IF NOT EXISTS mental_wellness_db;
USE mental_wellness_db;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Mood entries table — one row per detected/logged mood
CREATE TABLE IF NOT EXISTS mood_entries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    detected_emotion VARCHAR(30) NOT NULL,   -- e.g. happy, sad, angry, neutral, surprised, fearful, disgusted
    confidence FLOAT,                        -- 0.0 - 1.0 score from face-api.js
    note TEXT,                               -- optional user-added note
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Journal entries table — optional free-text wellness journal
CREATE TABLE IF NOT EXISTS journal_entries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(150),
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Wellness activities table — e.g. meditation, journaling, breathing exercise logs
CREATE TABLE IF NOT EXISTS wellness_activities (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    activity_type VARCHAR(50) NOT NULL,      -- e.g. meditation, breathing, journaling
    duration_minutes INT,
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Helpful index for querying a user's mood history by date range
CREATE INDEX idx_mood_user_time ON mood_entries(user_id, recorded_at);
