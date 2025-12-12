-- Base schema for standup/task tracker
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    role TEXT DEFAULT 'Developer'
);

CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    description TEXT NOT NULL,
    status TEXT DEFAULT 'PENDING',
    delay_risk TEXT DEFAULT 'UNKNOWN',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_tasks_user_id_created_at ON tasks (user_id, created_at DESC);

CREATE TABLE IF NOT EXISTS standups (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    yesterday TEXT NOT NULL,
    today TEXT NOT NULL,
    blockers TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_standups_user_id_created_at ON standups (user_id, created_at DESC);
