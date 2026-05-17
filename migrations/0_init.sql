CREATE TABLE IF NOT EXISTS documents (
    id TEXT PRIMARY KEY,
    filename TEXT NOT NULL,
    format TEXT NOT NULL,
    status TEXT NOT NULL,
    uploaded_at TEXT,
    started_at TEXT,
    completed_at TEXT
);

CREATE TABLE IF NOT EXISTS pages (
    id TEXT PRIMARY KEY,
    document_id TEXT NOT NULL,
    number INTEGER NOT NULL,
    markdown TEXT,
    FOREIGN KEY (document_id) REFERENCES documents (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS figures (
    page_id TEXT NOT NULL,
    kind TEXT NOT NULL,
    bouding_box TEXT NOT NULL,
    caption TEXT NOT NULL,
    order INT NOT NULL,
    FOREIGN KEY (page_id) REFERENCES pages (id) ON DELETE CASCADE
);


