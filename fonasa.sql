SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;


CREATE TABLE `atencion` (
  `id` int(11) NOT NULL,
  `id_paciente` int(11) NOT NULL,
  `id_consulta` int(11) NOT NULL,
  `observaciones` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `estado` varchar(255) COLLATE utf8_unicode_ci NOT NULL DEFAULT 'activo',
  `prioridad` int(11) NOT NULL,
  `en_espera` varchar(255) COLLATE utf8_unicode_ci NOT NULL DEFAULT 'en_espera' COMMENT 'en_espera, atendido o cancelado',
  `numero_atencion` int(11) NOT NULL,
  `estatura` int(11) DEFAULT NULL,
  `peso` int(11) DEFAULT NULL,
  `rel_peso_estatura` int(11) DEFAULT NULL,
  `tiene_dieta` tinyint(1) DEFAULT 0,
  `fumador` varchar(2) COLLATE utf8_unicode_ci DEFAULT NULL,
  `edad` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE `consulta` (
  `id` int(11) NOT NULL,
  `cant_pacientes` int(11) NOT NULL,
  `id_doctor` int(11) NOT NULL,
  `tipo_consulta` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `estado` tinyint(1) NOT NULL DEFAULT 1,
  `fecha_consulta` date NOT NULL,
  `id_hospital` int(11) NOT NULL,
  `ticket` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE `doctor` (
  `id` int(11) NOT NULL,
  `id_persona` int(11) NOT NULL,
  `especialidad` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `estado` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE `hospital` (
  `id` int(11) NOT NULL,
  `nombre` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `direccion` varchar(255) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE `paciente` (
  `id` int(11) NOT NULL,
  `id_persona` int(11) NOT NULL,
  `estado` varchar(255) COLLATE utf8_unicode_ci NOT NULL DEFAULT 'activo',
  `id_hospital` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE `personas` (
  `id` int(11) NOT NULL,
  `rut` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `nombre` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `direccion` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `estado` tinyint(1) NOT NULL DEFAULT 1,
  `fechaNacimiento` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE `sala_atencion` (
  `id` int(11) NOT NULL,
  `id_atencion` int(11) NOT NULL,
  `id_consulta` int(11) NOT NULL,
  `id_paciente` int(11) NOT NULL,
  `pendiente1` int(11) NOT NULL,
  `pendiente2` int(11) NOT NULL,
  `prioridad` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE `sala_espera` (
  `id` int(11) NOT NULL,
  `id_atencion` int(11) NOT NULL,
  `prioridad` int(11) NOT NULL,
  `id_consulta` int(11) NOT NULL,
  `id_paciente` int(11) NOT NULL,
  `pendiente1` int(11) NOT NULL,
  `pendiente2` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE `trabajo` (
  `id` int(11) NOT NULL,
  `id-hospital` int(11) NOT NULL,
  `id-doctor` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


ALTER TABLE `atencion`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id-consulta` (`id_consulta`),
  ADD KEY `id-paciente` (`id_paciente`);

ALTER TABLE `consulta`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id-doctor` (`id_doctor`),
  ADD KEY `id-hospital` (`id_hospital`);

ALTER TABLE `doctor`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id-persona` (`id_persona`);

ALTER TABLE `hospital`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `paciente`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id-persona` (`id_persona`),
  ADD KEY `paciente_ibfk_1` (`id_hospital`);

ALTER TABLE `personas`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `sala_atencion`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `sala_espera`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `trabajo`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id-doctor` (`id-doctor`),
  ADD KEY `id-hospital` (`id-hospital`);


ALTER TABLE `atencion`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `consulta`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `doctor`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `hospital`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `paciente`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `personas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `sala_atencion`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `sala_espera`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `trabajo`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;


ALTER TABLE `atencion`
  ADD CONSTRAINT `atencion_ibfk_1` FOREIGN KEY (`id_consulta`) REFERENCES `consulta` (`id`),
  ADD CONSTRAINT `atencion_ibfk_2` FOREIGN KEY (`id_paciente`) REFERENCES `paciente` (`id`);

ALTER TABLE `consulta`
  ADD CONSTRAINT `consulta_ibfk_1` FOREIGN KEY (`id_doctor`) REFERENCES `doctor` (`id`),
  ADD CONSTRAINT `consulta_ibfk_2` FOREIGN KEY (`id_hospital`) REFERENCES `hospital` (`id`);

ALTER TABLE `doctor`
  ADD CONSTRAINT `doctor_ibfk_1` FOREIGN KEY (`id_persona`) REFERENCES `personas` (`id`);

ALTER TABLE `paciente`
  ADD CONSTRAINT `paciente_ibfk_1` FOREIGN KEY (`id_hospital`) REFERENCES `hospital` (`id`);

ALTER TABLE `trabajo`
  ADD CONSTRAINT `trabajo_ibfk_1` FOREIGN KEY (`id-doctor`) REFERENCES `doctor` (`id`),
  ADD CONSTRAINT `trabajo_ibfk_2` FOREIGN KEY (`id-hospital`) REFERENCES `hospital` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
