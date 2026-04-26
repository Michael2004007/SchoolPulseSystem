CREATE DATABASE IF NOT EXISTS school_pulse_system;
USE school_pulse_system;

CREATE TABLE pulsera (
    id INT PRIMARY KEY,
    estado ENUM('disponible', 'repartida', 'pagada') DEFAULT 'disponible',
    fecha_creacion DATETIME DEFAULT NOW()
);

CREATE TABLE alumno (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    curso VARCHAR(50) NOT NULL
);

CREATE TABLE reparto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    alumno_id INT NOT NULL,
    pulsera_id INT NOT NULL,
    fecha_reparto DATETIME DEFAULT NOW(),
    FOREIGN KEY (alumno_id) REFERENCES alumno(id),
    FOREIGN KEY (pulsera_id) REFERENCES pulsera(id)
);

CREATE TABLE cobro (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pulsera_id INT NOT NULL,
    monto DECIMAL(10,2) NOT NULL,
    fecha_cobro DATETIME DEFAULT NOW(),
    FOREIGN KEY (pulsera_id) REFERENCES pulsera(id)
);