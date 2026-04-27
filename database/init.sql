CREATE TABLE tesis (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    estudiante VARCHAR(120) NOT NULL,
    director VARCHAR(120) NOT NULL,
    linea_investigacion VARCHAR(150),
    estado VARCHAR(50) DEFAULT 'en proceso',
    fecha_registro DATE DEFAULT CURRENT_DATE
);

CREATE TABLE avances (
    id SERIAL PRIMARY KEY,
    tesis_id INTEGER REFERENCES tesis(id) ON DELETE CASCADE,
    descripcion TEXT NOT NULL,
    porcentaje_avance INTEGER NOT NULL,
    observaciones TEXT,
    fecha DATE DEFAULT CURRENT_DATE
);

INSERT INTO tesis (titulo, estudiante, director, linea_investigacion, estado)
VALUES
('Sistema web de seguimiento de tesis', 'Ana Torres', 'Dr. Pérez', 'Ingeniería de Software', 'en proceso');
