CREATE TABLE IF NOT EXISTS persons (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    age INT
);

INSERT INTO persons (name, age) VALUES ('Asash', 34);
INSERT INTO persons (name, age) VALUES ('Leon', 25);
INSERT INTO persons (name, age) VALUES ('Omar', 35);