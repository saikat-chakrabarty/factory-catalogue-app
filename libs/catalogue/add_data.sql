CREATE TABLE IF NOT EXISTS factories
(
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(256) NOT NULL UNIQUE,
    location    VARCHAR(1024) NOT NULL,
    product     VARCHAR(256) NOT NULL
);

CREATE TABLE IF NOT EXISTS raw_materials
(
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(256) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS factory_raw_material
(
    factory_id          INTEGER NOT NULL REFERENCES factories (id) ON DELETE CASCADE,
    raw_material_id     INTEGER NOT NULL REFERENCES raw_materials (id) ON DELETE CASCADE
);