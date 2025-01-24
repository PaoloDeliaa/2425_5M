
-- CREATE DATABASE IF NOT EXISTS delia_albergo; 
USE delia_albergo;

-- Drop tables if they exist
DROP TABLE IF EXISTS CAMERAPRENOTAZIONE;
DROP TABLE IF EXISTS PRENOTAZIONE;
DROP TABLE IF EXISTS CAMERA;

CREATE TABLE CAMERA (
    numero INT PRIMARY KEY,
    tipo VARCHAR(50),
    disponibile BOOLEAN,
    prezzo INT,
    numero_posti INT
);

CREATE TABLE PRENOTAZIONE (
    id INT PRIMARY KEY,
    numero_camera INT,
    data_arrivo DATE,
    data_partenza DATE,
    nome_cliente VARCHAR(100),
    FOREIGN KEY (numero_camera) REFERENCES CAMERA(numero)
);

CREATE TABLE CAMERAPRENOTAZIONE (
    id_camera INT,
    id_prenotazione INT,
    PRIMARY KEY (id_camera, id_prenotazione),
    FOREIGN KEY (id_camera) REFERENCES CAMERA(numero),
    FOREIGN KEY (id_prenotazione) REFERENCES PRENOTAZIONE(id)
);

-- Insert mock data
INSERT INTO CAMERA (numero, tipo, disponibile, prezzo, numero_posti) VALUES
(101, 'Singola', TRUE, 50, 1),
(102, 'Doppia', TRUE, 80, 2),
(103, 'Suite', FALSE, 150, 4),
(104, 'Singola', TRUE, 50, 1),
(105, 'Doppia', TRUE, 80, 2),
(106, 'Suite', FALSE, 150, 4);

INSERT INTO PRENOTAZIONE (id, numero_camera, data_arrivo, data_partenza, nome_cliente) VALUES
(1, 103, '2023-10-01', '2023-10-05', 'Mario Rossi'),
(2, 106, '2023-10-10', '2023-10-15', 'Luigi Bianchi');

INSERT INTO CAMERAPRENOTAZIONE (id_camera, id_prenotazione) VALUES
(103, 1),
(106, 2);