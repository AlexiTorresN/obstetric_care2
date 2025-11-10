-- phpMyAdmin SQL Dump
-- version 4.9.1
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost
-- Tiempo de generación: 08-11-2025 a las 14:02:38
-- Versión del servidor: 8.0.17
-- Versión de PHP: 7.3.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `obstetric_carebdd`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add Ficha Obstétrica', 7, 'add_fichaobstetrica'),
(26, 'Can change Ficha Obstétrica', 7, 'change_fichaobstetrica'),
(27, 'Can delete Ficha Obstétrica', 7, 'delete_fichaobstetrica'),
(28, 'Can view Ficha Obstétrica', 7, 'view_fichaobstetrica'),
(29, 'Can add Ingreso de Paciente', 8, 'add_ingresopaciente'),
(30, 'Can change Ingreso de Paciente', 8, 'change_ingresopaciente'),
(31, 'Can delete Ingreso de Paciente', 8, 'delete_ingresopaciente'),
(32, 'Can view Ingreso de Paciente', 8, 'view_ingresopaciente'),
(33, 'Can add Medicamento de Ficha', 9, 'add_medicamentoficha'),
(34, 'Can change Medicamento de Ficha', 9, 'change_medicamentoficha'),
(35, 'Can delete Medicamento de Ficha', 9, 'delete_medicamentoficha'),
(36, 'Can view Medicamento de Ficha', 9, 'view_medicamentoficha'),
(37, 'Can add Administración de Medicamento', 10, 'add_administracionmedicamento'),
(38, 'Can change Administración de Medicamento', 10, 'change_administracionmedicamento'),
(39, 'Can delete Administración de Medicamento', 10, 'delete_administracionmedicamento'),
(40, 'Can view Administración de Medicamento', 10, 'view_administracionmedicamento'),
(41, 'Can add Patología', 11, 'add_patologias'),
(42, 'Can change Patología', 11, 'change_patologias'),
(43, 'Can delete Patología', 11, 'delete_patologias'),
(44, 'Can view Patología', 11, 'view_patologias'),
(45, 'Can add Registro TENS', 12, 'add_registrotens'),
(46, 'Can change Registro TENS', 12, 'change_registrotens'),
(47, 'Can delete Registro TENS', 12, 'delete_registrotens'),
(48, 'Can view Registro TENS', 12, 'view_registrotens'),
(49, 'Can add Tratamiento Aplicado', 13, 'add_tratamiento_aplicado'),
(50, 'Can change Tratamiento Aplicado', 13, 'change_tratamiento_aplicado'),
(51, 'Can delete Tratamiento Aplicado', 13, 'delete_tratamiento_aplicado'),
(52, 'Can view Tratamiento Aplicado', 13, 'view_tratamiento_aplicado'),
(53, 'Can add persona', 14, 'add_persona'),
(54, 'Can change persona', 14, 'change_persona'),
(55, 'Can delete persona', 14, 'delete_persona'),
(56, 'Can view persona', 14, 'view_persona'),
(57, 'Can add Paciente', 15, 'add_paciente'),
(58, 'Can change Paciente', 15, 'change_paciente'),
(59, 'Can delete Paciente', 15, 'delete_paciente'),
(60, 'Can view Paciente', 15, 'view_paciente'),
(61, 'Can add medico', 16, 'add_medico'),
(62, 'Can change medico', 16, 'change_medico'),
(63, 'Can delete medico', 16, 'delete_medico'),
(64, 'Can view medico', 16, 'view_medico'),
(65, 'Can add matrona', 17, 'add_matrona'),
(66, 'Can change matrona', 17, 'change_matrona'),
(67, 'Can delete matrona', 17, 'delete_matrona'),
(68, 'Can view matrona', 17, 'view_matrona'),
(69, 'Can add tens', 18, 'add_tens'),
(70, 'Can change tens', 18, 'change_tens'),
(71, 'Can delete tens', 18, 'delete_tens'),
(72, 'Can view tens', 18, 'view_tens'),
(73, 'Can add controles previos', 19, 'add_controlesprevios'),
(74, 'Can change controles previos', 19, 'change_controlesprevios'),
(75, 'Can delete controles previos', 19, 'delete_controlesprevios'),
(76, 'Can view controles previos', 19, 'view_controlesprevios'),
(77, 'Can add Registro de Parto', 20, 'add_registroparto'),
(78, 'Can change Registro de Parto', 20, 'change_registroparto'),
(79, 'Can delete Registro de Parto', 20, 'delete_registroparto'),
(80, 'Can view Registro de Parto', 20, 'view_registroparto'),
(81, 'Can add Ficha de Parto (Ingreso)', 21, 'add_fichaparto'),
(82, 'Can change Ficha de Parto (Ingreso)', 21, 'change_fichaparto'),
(83, 'Can delete Ficha de Parto (Ingreso)', 21, 'delete_fichaparto'),
(84, 'Can view Ficha de Parto (Ingreso)', 21, 'view_fichaparto'),
(85, 'Can add Registro de Recién Nacido', 22, 'add_registroreciennacido'),
(86, 'Can change Registro de Recién Nacido', 22, 'change_registroreciennacido'),
(87, 'Can delete Registro de Recién Nacido', 22, 'delete_registroreciennacido'),
(88, 'Can view Registro de Recién Nacido', 22, 'view_registroreciennacido'),
(89, 'Can add Documentos de Parto', 23, 'add_documentosparto'),
(90, 'Can change Documentos de Parto', 23, 'change_documentosparto'),
(91, 'Can delete Documentos de Parto', 23, 'delete_documentosparto'),
(92, 'Can view Documentos de Parto', 23, 'view_documentosparto');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(17, 'gestionApp', 'matrona'),
(16, 'gestionApp', 'medico'),
(15, 'gestionApp', 'paciente'),
(14, 'gestionApp', 'persona'),
(18, 'gestionApp', 'tens'),
(21, 'ingresoPartoApp', 'fichaparto'),
(19, 'legacyApp', 'controlesprevios'),
(10, 'matronaApp', 'administracionmedicamento'),
(7, 'matronaApp', 'fichaobstetrica'),
(8, 'matronaApp', 'ingresopaciente'),
(9, 'matronaApp', 'medicamentoficha'),
(11, 'medicoApp', 'patologias'),
(20, 'partosApp', 'registroparto'),
(23, 'recienNacidoApp', 'documentosparto'),
(22, 'recienNacidoApp', 'registroreciennacido'),
(6, 'sessions', 'session'),
(12, 'tensApp', 'registrotens'),
(13, 'tensApp', 'tratamiento_aplicado');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2025-11-08 14:01:47.940006'),
(2, 'auth', '0001_initial', '2025-11-08 14:01:48.421710'),
(3, 'admin', '0001_initial', '2025-11-08 14:01:48.564403'),
(4, 'admin', '0002_logentry_remove_auto_add', '2025-11-08 14:01:48.570163'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2025-11-08 14:01:48.575670'),
(6, 'contenttypes', '0002_remove_content_type_name', '2025-11-08 14:01:48.674526'),
(7, 'auth', '0002_alter_permission_name_max_length', '2025-11-08 14:01:48.763555'),
(8, 'auth', '0003_alter_user_email_max_length', '2025-11-08 14:01:48.815347'),
(9, 'auth', '0004_alter_user_username_opts', '2025-11-08 14:01:48.821354'),
(10, 'auth', '0005_alter_user_last_login_null', '2025-11-08 14:01:48.871377'),
(11, 'auth', '0006_require_contenttypes_0002', '2025-11-08 14:01:48.873655'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2025-11-08 14:01:48.879261'),
(13, 'auth', '0008_alter_user_username_max_length', '2025-11-08 14:01:48.936295'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2025-11-08 14:01:49.008198'),
(15, 'auth', '0010_alter_group_name_max_length', '2025-11-08 14:01:49.026101'),
(16, 'auth', '0011_update_proxy_permissions', '2025-11-08 14:01:49.032332'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2025-11-08 14:01:49.088417'),
(18, 'gestionApp', '0001_initial', '2025-11-08 14:01:49.495851'),
(19, 'medicoApp', '0001_initial', '2025-11-08 14:01:49.514823'),
(20, 'matronaApp', '0001_initial', '2025-11-08 14:01:50.253883'),
(21, 'ingresoPartoApp', '0001_initial', '2025-11-08 14:01:50.404360'),
(22, 'legacyApp', '0001_initial', '2025-11-08 14:01:50.407250'),
(23, 'partosApp', '0001_initial', '2025-11-08 14:01:50.613499'),
(24, 'recienNacidoApp', '0001_initial', '2025-11-08 14:01:50.845681'),
(25, 'sessions', '0001_initial', '2025-11-08 14:01:50.875113'),
(26, 'tensApp', '0001_initial', '2025-11-08 14:01:51.420738');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `gestionapp_matrona`
--

CREATE TABLE `gestionapp_matrona` (
  `id` bigint(20) NOT NULL,
  `Especialidad` varchar(100) NOT NULL,
  `Registro_medico` varchar(100) NOT NULL,
  `Años_experiencia` int(11) NOT NULL,
  `Turno` varchar(100) NOT NULL,
  `Activo` tinyint(1) NOT NULL,
  `persona_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `gestionapp_medico`
--

CREATE TABLE `gestionapp_medico` (
  `id` bigint(20) NOT NULL,
  `Especialidad` varchar(100) NOT NULL,
  `Registro_medico` varchar(100) NOT NULL,
  `Años_experiencia` int(11) NOT NULL,
  `Turno` varchar(100) NOT NULL,
  `Activo` tinyint(1) NOT NULL,
  `persona_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `gestionapp_paciente`
--

CREATE TABLE `gestionapp_paciente` (
  `persona_id` bigint(20) NOT NULL,
  `Estado_civil` varchar(20) NOT NULL,
  `Previcion` varchar(20) NOT NULL,
  `paridad` varchar(50) NOT NULL,
  `Ductus_Venosus` varchar(70) NOT NULL,
  `control_prenatal` tinyint(1) NOT NULL,
  `Consultorio` varchar(100) NOT NULL,
  `IMC` decimal(5,2) DEFAULT NULL,
  `Preeclampsia_Severa` tinyint(1) NOT NULL,
  `Eclampsia` tinyint(1) NOT NULL,
  `Sepsis_o_Infeccion_SiST` tinyint(1) NOT NULL,
  `Infeccion_Ovular_o_Corioamnionitis` tinyint(1) NOT NULL,
  `Acompañante` varchar(120) NOT NULL,
  `Contacto_emergencia` varchar(30) NOT NULL,
  `Fecha_y_Hora_Ingreso` datetime(6) NOT NULL,
  `activo` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `gestionapp_persona`
--

CREATE TABLE `gestionapp_persona` (
  `id` bigint(20) NOT NULL,
  `Rut` varchar(100) NOT NULL,
  `Nombre` varchar(100) NOT NULL,
  `Apellido_Paterno` varchar(100) NOT NULL,
  `Apellido_Materno` varchar(100) NOT NULL,
  `Fecha_nacimiento` date NOT NULL,
  `Sexo` varchar(100) NOT NULL,
  `Inmigrante` varchar(10) NOT NULL,
  `Nacionalidad` varchar(100) NOT NULL,
  `Pueblos_originarios` varchar(100) NOT NULL,
  `Discapacidad` varchar(10) NOT NULL,
  `Tipo_de_Discapacidad` varchar(200) DEFAULT NULL,
  `Privada_de_Libertad` varchar(10) NOT NULL,
  `Trans_Masculino` varchar(10) NOT NULL,
  `Telefono` varchar(100) NOT NULL,
  `Direccion` varchar(100) NOT NULL,
  `Email` varchar(100) NOT NULL,
  `Activo` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `gestionapp_tens`
--

CREATE TABLE `gestionapp_tens` (
  `id` bigint(20) NOT NULL,
  `Nivel` varchar(100) NOT NULL,
  `Años_experiencia` int(11) NOT NULL,
  `Turno` varchar(100) NOT NULL,
  `Certificaciones` varchar(100) NOT NULL,
  `Activo` tinyint(1) NOT NULL,
  `persona_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ingresopartoapp_fichaparto`
--

CREATE TABLE `ingresopartoapp_fichaparto` (
  `id` bigint(20) NOT NULL,
  `numero_ficha_parto` varchar(20) NOT NULL,
  `tipo_paciente` varchar(30) NOT NULL,
  `origen_ingreso` varchar(20) NOT NULL,
  `fecha_ingreso` date NOT NULL,
  `hora_ingreso` time(6) NOT NULL,
  `plan_de_parto` tinyint(1) NOT NULL,
  `visita_guiada` tinyint(1) NOT NULL,
  `control_prenatal` tinyint(1) NOT NULL,
  `consultorio_origen` varchar(200) NOT NULL,
  `preeclampsia_severa` tinyint(1) NOT NULL,
  `eclampsia` tinyint(1) NOT NULL,
  `sepsis_infeccion_grave` tinyint(1) NOT NULL,
  `infeccion_ovular` tinyint(1) NOT NULL,
  `otra_patologia` varchar(300) NOT NULL,
  `numero_aro` varchar(20) NOT NULL,
  `vih_tomado_prepartos` tinyint(1) NOT NULL,
  `vih_tomado_sala` tinyint(1) NOT NULL,
  `vih_orden_toma` varchar(1) NOT NULL,
  `sgb_pesquisa` tinyint(1) NOT NULL,
  `sgb_resultado` varchar(10) NOT NULL,
  `antibiotico_sgb` tinyint(1) NOT NULL,
  `vdrl_resultado` varchar(15) NOT NULL,
  `tratamiento_sifilis` tinyint(1) NOT NULL,
  `hepatitis_b_tomado` tinyint(1) NOT NULL,
  `derivacion_gastro` tinyint(1) NOT NULL,
  `fecha_creacion` datetime(6) NOT NULL,
  `fecha_modificacion` datetime(6) NOT NULL,
  `activa` tinyint(1) NOT NULL,
  `ficha_obstetrica_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `matronaapp_administracionmedicamento`
--

CREATE TABLE `matronaapp_administracionmedicamento` (
  `id` bigint(20) NOT NULL,
  `fecha_hora_administracion` datetime(6) NOT NULL,
  `se_realizo_lavado` tinyint(1) NOT NULL,
  `observaciones` longtext NOT NULL,
  `reacciones_adversas` longtext NOT NULL,
  `administrado_exitosamente` tinyint(1) NOT NULL,
  `motivo_no_administracion` longtext NOT NULL,
  `fecha_registro` datetime(6) NOT NULL,
  `tens_id` bigint(20) NOT NULL,
  `medicamento_ficha_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `matronaapp_fichaobstetrica`
--

CREATE TABLE `matronaapp_fichaobstetrica` (
  `id` bigint(20) NOT NULL,
  `numero_ficha` varchar(20) NOT NULL,
  `nombre_acompanante` varchar(200) NOT NULL,
  `numero_gestas` int(11) NOT NULL,
  `numero_partos` int(11) NOT NULL,
  `partos_vaginales` int(11) NOT NULL,
  `partos_cesareas` int(11) NOT NULL,
  `numero_abortos` int(11) NOT NULL,
  `nacidos_vivos` int(11) NOT NULL,
  `fecha_ultima_regla` date DEFAULT NULL,
  `fecha_probable_parto` date DEFAULT NULL,
  `edad_gestacional_semanas` int(11) DEFAULT NULL,
  `edad_gestacional_dias` int(11) DEFAULT NULL,
  `peso_actual` decimal(5,2) DEFAULT NULL,
  `talla` decimal(5,2) DEFAULT NULL,
  `descripcion_patologias` longtext NOT NULL,
  `patologias_criticas` varchar(100) NOT NULL,
  `vih_tomado` tinyint(1) NOT NULL,
  `vih_resultado` varchar(20) NOT NULL,
  `vih_aro` varchar(50) NOT NULL,
  `sgb_pesquisa` tinyint(1) NOT NULL,
  `sgb_resultado` varchar(20) NOT NULL,
  `sgb_antibiotico` varchar(100) NOT NULL,
  `vdrl_resultado` varchar(20) NOT NULL,
  `vdrl_tratamiento_atb` tinyint(1) NOT NULL,
  `hepatitis_b_tomado` tinyint(1) NOT NULL,
  `hepatitis_b_resultado` varchar(20) NOT NULL,
  `hepatitis_b_derivacion` tinyint(1) NOT NULL,
  `observaciones` longtext NOT NULL,
  `antecedentes_relevantes` longtext NOT NULL,
  `fecha_creacion` datetime(6) NOT NULL,
  `fecha_modificacion` datetime(6) NOT NULL,
  `activa` tinyint(1) NOT NULL,
  `matrona_responsable_id` bigint(20) NOT NULL,
  `paciente_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `matronaapp_fichaobstetrica_patologias`
--

CREATE TABLE `matronaapp_fichaobstetrica_patologias` (
  `id` bigint(20) NOT NULL,
  `fichaobstetrica_id` bigint(20) NOT NULL,
  `patologias_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `matronaapp_ingresopaciente`
--

CREATE TABLE `matronaapp_ingresopaciente` (
  `id` bigint(20) NOT NULL,
  `motivo_ingreso` longtext NOT NULL,
  `fecha_ingreso` date NOT NULL,
  `hora_ingreso` time(6) NOT NULL,
  `edad_gestacional_semanas` int(11) DEFAULT NULL,
  `derivacion` varchar(200) NOT NULL,
  `observaciones` longtext NOT NULL,
  `numero_ficha` varchar(20) NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `paciente_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `matronaapp_medicamentoficha`
--

CREATE TABLE `matronaapp_medicamentoficha` (
  `id` bigint(20) NOT NULL,
  `nombre_medicamento` varchar(200) NOT NULL,
  `dosis` varchar(100) NOT NULL,
  `via_administracion` varchar(50) NOT NULL,
  `frecuencia` varchar(50) NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_termino` date NOT NULL,
  `observaciones` longtext NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `fecha_registro` datetime(6) NOT NULL,
  `ficha_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `medicoapp_patologias`
--

CREATE TABLE `medicoapp_patologias` (
  `id` bigint(20) NOT NULL,
  `nombre` varchar(200) NOT NULL,
  `codigo_cie_10` varchar(100) NOT NULL,
  `descripcion` longtext,
  `nivel_de_riesgo` varchar(20) NOT NULL,
  `protocolo_seguimiento` longtext,
  `estado` varchar(10) NOT NULL,
  `fecha_creacion` datetime(6) NOT NULL,
  `fecha_modificacion` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `partosapp_registroparto`
--

CREATE TABLE `partosapp_registroparto` (
  `id` bigint(20) NOT NULL,
  `numero_registro` varchar(20) NOT NULL,
  `fecha_hora_admision` datetime(6) NOT NULL,
  `fecha_hora_parto` datetime(6) DEFAULT NULL,
  `vih_tomado_prepartos` tinyint(1) NOT NULL,
  `vih_tomado_sala` varchar(20) NOT NULL,
  `edad_gestacional_semanas` int(11) NOT NULL,
  `edad_gestacional_dias` int(11) NOT NULL,
  `monitor_ttc` tinyint(1) NOT NULL,
  `induccion` tinyint(1) NOT NULL,
  `aceleracion_correccion` tinyint(1) NOT NULL,
  `numero_tactos_vaginales` int(11) NOT NULL,
  `rotura_membrana` varchar(10) NOT NULL,
  `tiempo_membranas_rotas` int(11) DEFAULT NULL,
  `tiempo_dilatacion` int(11) DEFAULT NULL,
  `tiempo_expulsivo` int(11) DEFAULT NULL,
  `libertad_movimiento` tinyint(1) NOT NULL,
  `tipo_regimen` varchar(10) NOT NULL,
  `tipo_parto` varchar(20) NOT NULL,
  `alumbramiento_dirigido` tinyint(1) NOT NULL,
  `clasificacion_robson` varchar(30) NOT NULL,
  `posicion_materna_parto` varchar(20) NOT NULL,
  `ofrecimiento_posiciones_alternativas` tinyint(1) NOT NULL,
  `estado_perine` varchar(20) NOT NULL,
  `esterilizacion` tinyint(1) NOT NULL,
  `revision` tinyint(1) NOT NULL,
  `inercia_uterina` tinyint(1) NOT NULL,
  `restos_placentarios` tinyint(1) NOT NULL,
  `trauma` tinyint(1) NOT NULL,
  `alteracion_coagulacion` tinyint(1) NOT NULL,
  `manejo_quirurgico_inercia` tinyint(1) NOT NULL,
  `histerectomia_obstetrica` tinyint(1) NOT NULL,
  `transfusion_sanguinea` tinyint(1) NOT NULL,
  `anestesia_neuroaxial` tinyint(1) NOT NULL,
  `oxido_nitroso` tinyint(1) NOT NULL,
  `analgesia_endovenosa` tinyint(1) NOT NULL,
  `anestesia_general` tinyint(1) NOT NULL,
  `anestesia_local` tinyint(1) NOT NULL,
  `analgesia_no_farmacologica` tinyint(1) NOT NULL,
  `balon_kinesico` tinyint(1) NOT NULL,
  `lenteja_parto` tinyint(1) NOT NULL,
  `rebozo` tinyint(1) NOT NULL,
  `aromaterapia` tinyint(1) NOT NULL,
  `peridural_solicitada_paciente` tinyint(1) NOT NULL,
  `peridural_indicada_medico` tinyint(1) NOT NULL,
  `peridural_administrada` tinyint(1) NOT NULL,
  `tiempo_espera_peridural` int(11) DEFAULT NULL,
  `profesional_responsable` varchar(200) NOT NULL,
  `alumno` varchar(200) NOT NULL,
  `causa_cesarea` longtext NOT NULL,
  `observaciones` longtext NOT NULL,
  `uso_sala_saip` tinyint(1) NOT NULL,
  `fecha_creacion` datetime(6) NOT NULL,
  `fecha_modificacion` datetime(6) NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `ficha_id` bigint(20) NOT NULL,
  `ficha_ingreso_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reciennacidoapp_documentosparto`
--

CREATE TABLE `reciennacidoapp_documentosparto` (
  `id` bigint(20) NOT NULL,
  `recuerdos_entregados` longtext NOT NULL,
  `retira_placenta` tinyint(1) NOT NULL,
  `estampado_placenta` tinyint(1) NOT NULL,
  `folio_valido` varchar(50) NOT NULL,
  `folios_nulos` varchar(200) NOT NULL,
  `manejo_dolor_no_farmacologico` longtext NOT NULL,
  `fecha_creacion` datetime(6) NOT NULL,
  `fecha_modificacion` datetime(6) NOT NULL,
  `registro_recien_nacido_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reciennacidoapp_registroreciennacido`
--

CREATE TABLE `reciennacidoapp_registroreciennacido` (
  `id` bigint(20) NOT NULL,
  `sexo` varchar(20) NOT NULL,
  `peso` int(11) NOT NULL,
  `talla` int(11) NOT NULL,
  `ligadura_tardia_cordon` tinyint(1) NOT NULL,
  `apgar_1_minuto` int(11) NOT NULL,
  `apgar_5_minutos` int(11) NOT NULL,
  `fecha_nacimiento` datetime(6) NOT NULL,
  `tiempo_apego` int(11) DEFAULT NULL,
  `apego_canguro` tinyint(1) NOT NULL,
  `acompanamiento_preparto` tinyint(1) NOT NULL,
  `acompanamiento_parto` tinyint(1) NOT NULL,
  `acompanamiento_rn` tinyint(1) NOT NULL,
  `motivo_no_acompanado` varchar(20) NOT NULL,
  `persona_acompanante` varchar(10) NOT NULL,
  `acompanante_secciona_cordon` tinyint(1) NOT NULL,
  `fecha_creacion` datetime(6) NOT NULL,
  `registro_parto_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tensapp_registrotens`
--

CREATE TABLE `tensapp_registrotens` (
  `id` bigint(20) NOT NULL,
  `fecha` date NOT NULL,
  `turno` varchar(10) NOT NULL,
  `temperatura` decimal(4,1) DEFAULT NULL,
  `frecuencia_cardiaca` int(10) UNSIGNED DEFAULT NULL,
  `presion_arterial_sistolica` int(10) UNSIGNED DEFAULT NULL,
  `presion_arterial_diastolica` int(10) UNSIGNED DEFAULT NULL,
  `frecuencia_respiratoria` int(10) UNSIGNED DEFAULT NULL,
  `saturacion_oxigeno` int(10) UNSIGNED DEFAULT NULL,
  `observaciones` longtext NOT NULL,
  `fecha_registro` datetime(6) NOT NULL,
  `ficha_id` bigint(20) NOT NULL,
  `tens_responsable_id` bigint(20) DEFAULT NULL
) ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tensapp_tratamiento_aplicado`
--

CREATE TABLE `tensapp_tratamiento_aplicado` (
  `id` bigint(20) NOT NULL,
  `nombre_medicamento` varchar(200) NOT NULL,
  `dosis` varchar(100) NOT NULL,
  `via_administracion` varchar(50) NOT NULL,
  `fecha_aplicacion` date NOT NULL,
  `hora_aplicacion` time(6) NOT NULL,
  `se_realizo_lavado_manos` tinyint(1) NOT NULL,
  `aplicado_exitosamente` tinyint(1) NOT NULL,
  `motivo_no_aplicacion` longtext NOT NULL,
  `observaciones` longtext NOT NULL,
  `reacciones_adversas` longtext NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `fecha_registro` datetime(6) NOT NULL,
  `fecha_modificacion` datetime(6) NOT NULL,
  `ficha_id` bigint(20) NOT NULL,
  `medicamento_ficha_id` bigint(20) DEFAULT NULL,
  `paciente_id` bigint(20) NOT NULL,
  `tens_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indices de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indices de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indices de la tabla `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indices de la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indices de la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indices de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indices de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indices de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indices de la tabla `gestionapp_matrona`
--
ALTER TABLE `gestionapp_matrona`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `Registro_medico` (`Registro_medico`),
  ADD UNIQUE KEY `persona_id` (`persona_id`);

--
-- Indices de la tabla `gestionapp_medico`
--
ALTER TABLE `gestionapp_medico`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `Registro_medico` (`Registro_medico`),
  ADD UNIQUE KEY `persona_id` (`persona_id`);

--
-- Indices de la tabla `gestionapp_paciente`
--
ALTER TABLE `gestionapp_paciente`
  ADD PRIMARY KEY (`persona_id`);

--
-- Indices de la tabla `gestionapp_persona`
--
ALTER TABLE `gestionapp_persona`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `Rut` (`Rut`);

--
-- Indices de la tabla `gestionapp_tens`
--
ALTER TABLE `gestionapp_tens`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `persona_id` (`persona_id`);

--
-- Indices de la tabla `ingresopartoapp_fichaparto`
--
ALTER TABLE `ingresopartoapp_fichaparto`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `numero_ficha_parto` (`numero_ficha_parto`),
  ADD KEY `ingresoPart_numero__40195a_idx` (`numero_ficha_parto`),
  ADD KEY `ingresoPart_ficha_o_a0a95f_idx` (`ficha_obstetrica_id`,`DESC`);

--
-- Indices de la tabla `matronaapp_administracionmedicamento`
--
ALTER TABLE `matronaapp_administracionmedicamento`
  ADD PRIMARY KEY (`id`),
  ADD KEY `matronaApp__medicam_81588c_idx` (`medicamento_ficha_id`,`DESC`),
  ADD KEY `matronaApp__tens_id_1ed7c8_idx` (`tens_id`,`DESC`);

--
-- Indices de la tabla `matronaapp_fichaobstetrica`
--
ALTER TABLE `matronaapp_fichaobstetrica`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `numero_ficha` (`numero_ficha`),
  ADD KEY `matronaApp__numero__6ad75a_idx` (`numero_ficha`),
  ADD KEY `matronaApp__pacient_7cc52c_idx` (`paciente_id`,`activa`),
  ADD KEY `matronaApp__fecha_c_ce7cca_idx` (`DESC`),
  ADD KEY `matronaApp_fichaobst_matrona_responsable__533d7e49_fk_gestionAp` (`matrona_responsable_id`);

--
-- Indices de la tabla `matronaapp_fichaobstetrica_patologias`
--
ALTER TABLE `matronaapp_fichaobstetrica_patologias`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `matronaApp_fichaobstetri_fichaobstetrica_id_patol_3d03ced6_uniq` (`fichaobstetrica_id`,`patologias_id`),
  ADD KEY `matronaApp_fichaobst_patologias_id_6c87d888_fk_medicoApp` (`patologias_id`);

--
-- Indices de la tabla `matronaapp_ingresopaciente`
--
ALTER TABLE `matronaapp_ingresopaciente`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `numero_ficha` (`numero_ficha`),
  ADD KEY `matronaApp_ingresopa_paciente_id_fb92cea3_fk_gestionAp` (`paciente_id`);

--
-- Indices de la tabla `matronaapp_medicamentoficha`
--
ALTER TABLE `matronaapp_medicamentoficha`
  ADD PRIMARY KEY (`id`),
  ADD KEY `matronaApp__ficha_i_e18c9f_idx` (`ficha_id`,`activo`);

--
-- Indices de la tabla `medicoapp_patologias`
--
ALTER TABLE `medicoapp_patologias`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `partosapp_registroparto`
--
ALTER TABLE `partosapp_registroparto`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `numero_registro` (`numero_registro`),
  ADD UNIQUE KEY `ficha_ingreso_id` (`ficha_ingreso_id`),
  ADD KEY `partosApp_r_numero__f4bca4_idx` (`numero_registro`),
  ADD KEY `partosApp_r_ficha_i_51cd4e_idx` (`ficha_id`,`DESC`),
  ADD KEY `partosApp_r_fecha_h_6ada6e_idx` (`DESC`);

--
-- Indices de la tabla `reciennacidoapp_documentosparto`
--
ALTER TABLE `reciennacidoapp_documentosparto`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `registro_recien_nacido_id` (`registro_recien_nacido_id`);

--
-- Indices de la tabla `reciennacidoapp_registroreciennacido`
--
ALTER TABLE `reciennacidoapp_registroreciennacido`
  ADD PRIMARY KEY (`id`),
  ADD KEY `recienNacid_registr_11b649_idx` (`registro_parto_id`,`DESC`);

--
-- Indices de la tabla `tensapp_registrotens`
--
ALTER TABLE `tensapp_registrotens`
  ADD PRIMARY KEY (`id`),
  ADD KEY `tensApp_reg_ficha_i_bae3e8_idx` (`ficha_id`,`DESC`),
  ADD KEY `tensApp_reg_tens_re_e52f43_idx` (`tens_responsable_id`,`DESC`);

--
-- Indices de la tabla `tensapp_tratamiento_aplicado`
--
ALTER TABLE `tensapp_tratamiento_aplicado`
  ADD PRIMARY KEY (`id`),
  ADD KEY `tensApp_tra_ficha_i_f30b2b_idx` (`ficha_id`,`DESC`),
  ADD KEY `tensApp_tra_pacient_d9fdb4_idx` (`paciente_id`,`DESC`),
  ADD KEY `tensApp_tra_tens_id_0e1028_idx` (`tens_id`,`DESC`),
  ADD KEY `tensApp_tra_medicam_5aee8f_idx` (`medicamento_ficha_id`,`DESC`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=93;

--
-- AUTO_INCREMENT de la tabla `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT de la tabla `gestionapp_matrona`
--
ALTER TABLE `gestionapp_matrona`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `gestionapp_medico`
--
ALTER TABLE `gestionapp_medico`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `gestionapp_persona`
--
ALTER TABLE `gestionapp_persona`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `gestionapp_tens`
--
ALTER TABLE `gestionapp_tens`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `ingresopartoapp_fichaparto`
--
ALTER TABLE `ingresopartoapp_fichaparto`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `matronaapp_administracionmedicamento`
--
ALTER TABLE `matronaapp_administracionmedicamento`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `matronaapp_fichaobstetrica`
--
ALTER TABLE `matronaapp_fichaobstetrica`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `matronaapp_fichaobstetrica_patologias`
--
ALTER TABLE `matronaapp_fichaobstetrica_patologias`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `matronaapp_ingresopaciente`
--
ALTER TABLE `matronaapp_ingresopaciente`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `matronaapp_medicamentoficha`
--
ALTER TABLE `matronaapp_medicamentoficha`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `medicoapp_patologias`
--
ALTER TABLE `medicoapp_patologias`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `partosapp_registroparto`
--
ALTER TABLE `partosapp_registroparto`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `reciennacidoapp_documentosparto`
--
ALTER TABLE `reciennacidoapp_documentosparto`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `reciennacidoapp_registroreciennacido`
--
ALTER TABLE `reciennacidoapp_registroreciennacido`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `tensapp_registrotens`
--
ALTER TABLE `tensapp_registrotens`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `tensapp_tratamiento_aplicado`
--
ALTER TABLE `tensapp_tratamiento_aplicado`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Filtros para la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Filtros para la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `gestionapp_matrona`
--
ALTER TABLE `gestionapp_matrona`
  ADD CONSTRAINT `gestionApp_matrona_persona_id_b143a671_fk_gestionApp_persona_id` FOREIGN KEY (`persona_id`) REFERENCES `gestionapp_persona` (`id`);

--
-- Filtros para la tabla `gestionapp_medico`
--
ALTER TABLE `gestionapp_medico`
  ADD CONSTRAINT `gestionApp_medico_persona_id_3b0312c0_fk_gestionApp_persona_id` FOREIGN KEY (`persona_id`) REFERENCES `gestionapp_persona` (`id`);

--
-- Filtros para la tabla `gestionapp_paciente`
--
ALTER TABLE `gestionapp_paciente`
  ADD CONSTRAINT `gestionApp_paciente_persona_id_f8914334_fk_gestionApp_persona_id` FOREIGN KEY (`persona_id`) REFERENCES `gestionapp_persona` (`id`);

--
-- Filtros para la tabla `gestionapp_tens`
--
ALTER TABLE `gestionapp_tens`
  ADD CONSTRAINT `gestionApp_tens_persona_id_ba3cf6dc_fk_gestionApp_persona_id` FOREIGN KEY (`persona_id`) REFERENCES `gestionapp_persona` (`id`);

--
-- Filtros para la tabla `ingresopartoapp_fichaparto`
--
ALTER TABLE `ingresopartoapp_fichaparto`
  ADD CONSTRAINT `ingresoPartoApp_fich_ficha_obstetrica_id_ec0a44a0_fk_matronaAp` FOREIGN KEY (`ficha_obstetrica_id`) REFERENCES `matronaapp_fichaobstetrica` (`id`);

--
-- Filtros para la tabla `matronaapp_administracionmedicamento`
--
ALTER TABLE `matronaapp_administracionmedicamento`
  ADD CONSTRAINT `matronaApp_administr_medicamento_ficha_id_f23c8300_fk_matronaAp` FOREIGN KEY (`medicamento_ficha_id`) REFERENCES `matronaapp_medicamentoficha` (`id`),
  ADD CONSTRAINT `matronaApp_administr_tens_id_7b3ac428_fk_gestionAp` FOREIGN KEY (`tens_id`) REFERENCES `gestionapp_tens` (`id`);

--
-- Filtros para la tabla `matronaapp_fichaobstetrica`
--
ALTER TABLE `matronaapp_fichaobstetrica`
  ADD CONSTRAINT `matronaApp_fichaobst_matrona_responsable__533d7e49_fk_gestionAp` FOREIGN KEY (`matrona_responsable_id`) REFERENCES `gestionapp_matrona` (`id`),
  ADD CONSTRAINT `matronaApp_fichaobst_paciente_id_f038737a_fk_gestionAp` FOREIGN KEY (`paciente_id`) REFERENCES `gestionapp_paciente` (`persona_id`);

--
-- Filtros para la tabla `matronaapp_fichaobstetrica_patologias`
--
ALTER TABLE `matronaapp_fichaobstetrica_patologias`
  ADD CONSTRAINT `matronaApp_fichaobst_fichaobstetrica_id_3bf754a1_fk_matronaAp` FOREIGN KEY (`fichaobstetrica_id`) REFERENCES `matronaapp_fichaobstetrica` (`id`),
  ADD CONSTRAINT `matronaApp_fichaobst_patologias_id_6c87d888_fk_medicoApp` FOREIGN KEY (`patologias_id`) REFERENCES `medicoapp_patologias` (`id`);

--
-- Filtros para la tabla `matronaapp_ingresopaciente`
--
ALTER TABLE `matronaapp_ingresopaciente`
  ADD CONSTRAINT `matronaApp_ingresopa_paciente_id_fb92cea3_fk_gestionAp` FOREIGN KEY (`paciente_id`) REFERENCES `gestionapp_paciente` (`persona_id`);

--
-- Filtros para la tabla `matronaapp_medicamentoficha`
--
ALTER TABLE `matronaapp_medicamentoficha`
  ADD CONSTRAINT `matronaApp_medicamen_ficha_id_6b5bf4e6_fk_matronaAp` FOREIGN KEY (`ficha_id`) REFERENCES `matronaapp_fichaobstetrica` (`id`);

--
-- Filtros para la tabla `partosapp_registroparto`
--
ALTER TABLE `partosapp_registroparto`
  ADD CONSTRAINT `partosApp_registropa_ficha_id_0484eb4b_fk_matronaAp` FOREIGN KEY (`ficha_id`) REFERENCES `matronaapp_fichaobstetrica` (`id`),
  ADD CONSTRAINT `partosApp_regMarkdown Preview Mermaid Supportistropa_ficha_ingreso_id_d3fbde3d_fk_ingresoPa` FOREIGN KEY (`ficha_ingreso_id`) REFERENCES `ingresopartoapp_fichaparto` (`id`);

--
-- Filtros para la tabla `reciennacidoapp_documentosparto`
--
ALTER TABLE `reciennacidoapp_documentosparto`
  ADD CONSTRAINT `recienNacidoApp_docu_registro_recien_naci_89e2a34e_fk_recienNac` FOREIGN KEY (`registro_recien_nacido_id`) REFERENCES `reciennacidoapp_registroreciennacido` (`id`);

--
-- Filtros para la tabla `reciennacidoapp_registroreciennacido`
--
ALTER TABLE `reciennacidoapp_registroreciennacido`
  ADD CONSTRAINT `recienNacidoApp_regi_registro_parto_id_bc552749_fk_partosApp` FOREIGN KEY (`registro_parto_id`) REFERENCES `partosapp_registroparto` (`id`);

--
-- Filtros para la tabla `tensapp_registrotens`
--
ALTER TABLE `tensapp_registrotens`
  ADD CONSTRAINT `tensApp_registrotens_ficha_id_482a1229_fk_matronaAp` FOREIGN KEY (`ficha_id`) REFERENCES `matronaapp_fichaobstetrica` (`id`),
  ADD CONSTRAINT `tensApp_registrotens_tens_responsable_id_197148d8_fk_gestionAp` FOREIGN KEY (`tens_responsable_id`) REFERENCES `gestionapp_tens` (`id`);

--
-- Filtros para la tabla `tensapp_tratamiento_aplicado`
--
ALTER TABLE `tensapp_tratamiento_aplicado`
  ADD CONSTRAINT `tensApp_tratamiento__ficha_id_459b6842_fk_matronaAp` FOREIGN KEY (`ficha_id`) REFERENCES `matronaapp_fichaobstetrica` (`id`),
  ADD CONSTRAINT `tensApp_tratamiento__medicamento_ficha_id_8fd148a0_fk_matronaAp` FOREIGN KEY (`medicamento_ficha_id`) REFERENCES `matronaapp_medicamentoficha` (`id`),
  ADD CONSTRAINT `tensApp_tratamiento__paciente_id_d5c579fd_fk_gestionAp` FOREIGN KEY (`paciente_id`) REFERENCES `gestionapp_paciente` (`persona_id`),
  ADD CONSTRAINT `tensApp_tratamiento__tens_id_36d8c832_fk_gestionAp` FOREIGN KEY (`tens_id`) REFERENCES `gestionapp_tens` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
