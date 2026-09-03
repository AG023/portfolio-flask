CREATE TABLE IF NOT EXISTS interests (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    category VARCHAR(100) NOT NULL,
    description TEXT NOT NULL
);

INSERT INTO interests (name, category, description)
VALUES
    ('Programmeren', 'Technologie', 'Ik maak graag websites en applicaties.'),
    ('Voetbal', 'Sport', 'Ik speel en kijk graag naar voetbal.'),
    ('Fortnite', 'Games', 'Ik speel graag fFortnite op mijn pc.')
ON CONFLICT (name) DO NOTHING;