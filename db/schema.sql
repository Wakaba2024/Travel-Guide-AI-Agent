CREATE TABLE destinations (
    id SERIAL PRIMARY KEY,
    name TEXT,
    county TEXT,
    category TEXT,
    description TEXT,
    source TEXT,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE travel_packages (
    id SERIAL PRIMARY KEY,
    company TEXT,
    destination TEXT,
    price NUMERIC,
    duration TEXT,
    description TEXT,
    source TEXT,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    name TEXT,
    location TEXT,
    event_date DATE,
    description TEXT,
    source TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE social_trends (
    id SERIAL PRIMARY KEY,
    platform TEXT,
    keyword TEXT,
    mention_count INT,
    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);