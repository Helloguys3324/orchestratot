-- Moderation logs table
CREATE TABLE IF NOT EXISTS moderation_logs (
    id SERIAL PRIMARY KEY,
    message_id VARCHAR(255) NOT NULL,
    author_id VARCHAR(255) NOT NULL,
    content TEXT,
    reason TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_moderation_logs_author ON moderation_logs(author_id);