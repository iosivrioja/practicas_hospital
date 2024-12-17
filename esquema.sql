

-- Tabla para Áreas
CREATE TABLE Area (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT, 
    estado VARCHAR(255) NOT NULL
);

-- Tabla para Sub-Áreas
CREATE TABLE SubArea (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT, 
    estado VARCHAR(255) NOT NULL,
    area_id INT,
    CONSTRAINT fk_area FOREIGN KEY (area_id) REFERENCES Area(id)
);

-- Tabla para Tipos de Equipo
CREATE TABLE TipoEquipo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT, 
    estado VARCHAR(255) NOT NULL
);

-- Tabla para Equipos
CREATE TABLE Equipo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo_patrimonial CHAR(11) UNIQUE NOT NULL,
    tipo_equipo_id INT,
    procesador VARCHAR(255),
    memoria_ram VARCHAR(255),
    sistema_operativo VARCHAR(255),
    subarea_id INT,
    almacenamiento VARCHAR(255),
    estado VARCHAR(255),
    CONSTRAINT fk_tipo_equipo FOREIGN KEY (tipo_equipo_id) REFERENCES TipoEquipo(id),
    CONSTRAINT fk_subarea_equipo FOREIGN KEY (subarea_id) REFERENCES SubArea(id)
);

-- Tabla para Partes
CREATE TABLE Parte (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT, 
    estado VARCHAR(255) NOT NULL,
    equipo_id INT,
    CONSTRAINT fk_equipo FOREIGN KEY (equipo_id) REFERENCES Equipo(id)
);

-- Tabla para Agentes
CREATE TABLE Agente (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    telefono VARCHAR(9), 
    estado VARCHAR(255) NOT NULL
);

-- Tabla de usuarios
CREATE TABLE Usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    contrasena VARCHAR(255) NOT NULL,
    rol VARCHAR(255) NOT NULL,
    estado VARCHAR(10)
);
