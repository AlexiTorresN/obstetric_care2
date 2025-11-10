CREATE DATABASE IF NOT EXISTS legacy_obstetric CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE legacy_obstetric;

CREATE TABLE `controles_previos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `paciente_rut` varchar(12) NOT NULL,
  `fecha_control` date NOT NULL,
  `semanas_gestacion` int(11) DEFAULT NULL,
  `presion_sistolica` int(11) DEFAULT NULL,
  `presion_diastolica` int(11) DEFAULT NULL,
  `peso_kg` decimal(5,2) DEFAULT NULL,
  `altura_uterina_cm` decimal(5,2) DEFAULT NULL,
  `fcf_lpm` int(11) DEFAULT NULL,
  `glucosa_mg_dl` decimal(6,2) DEFAULT NULL,
  `proteinuria` varchar(10) DEFAULT NULL,
  `observaciones` text,
  PRIMARY KEY (`id`),
  KEY `paciente_rut` (`paciente_rut`),
  KEY `fecha_control` (`fecha_control`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `controles_previos` (`id`, `paciente_rut`, `fecha_control`, `semanas_gestacion`, `presion_sistolica`, `presion_diastolica`, `peso_kg`, `altura_uterina_cm`, `fcf_lpm`, `glucosa_mg_dl`, `proteinuria`, `observaciones`) VALUES
(1, '16293109-1', '2021-09-10', 24, 110, 70, '67.40', '22.00', 150, '86.00', 'negativo', 'Control sin hallazgos'),
(2, '16293109-1', '2021-10-15', 28, 112, 72, '68.10', '26.00', 148, '92.00', 'negativo', 'Ganancia pondo-estatural adecuada'),
(3, '16293109-1', '2025-03-05', 20, 108, 68, '66.20', '20.00', 152, '85.00', 'negativo', 'Control sin hallazgos'),
(4, '16293109-1', '2025-04-09', 24, 112, 70, '67.00', '24.00', 148, '90.00', 'negativo', 'AU acorde a EG'),
(5, '16293109-1', '2025-05-14', 28, 116, 74, '68.50', '27.00', 146, '92.00', 'negativo', 'Glucosa dentro de rangos');
