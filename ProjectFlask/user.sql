-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 29-03-2023 a las 22:10:55
-- Versión del servidor: 8.0.32
-- Versión de PHP: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `usuario`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `user`
--

CREATE TABLE `user` (
  `ID` int NOT NULL,
  `name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `last_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `email` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `password` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `document` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `super_user` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `user`
--

INSERT INTO `user` (`ID`, `name`, `last_name`, `email`, `password`, `document`, `super_user`) VALUES
(1, 'Andres', 'Fonseca', 'affonseca613@misena.edu.co', 'pbkdf2:sha256:260000$xVXyNk252mbeLrTl$52ba835636ae4e51e2e939ee4c1106fbdc7c768ef3b27ea52a60174f360b7bf1', '1053605316', 1),
(4, 'Miguel', 'Rodriguez', 'miguel123@misena.edu.co', 'pbkdf2:sha256:260000$IghjnsqDX7mkMRbV$5009bce8c0786df3a7d724f8ddf8c0b260984efb2bfac04617aaa2850bba0a52', '132354534', 0),
(5, 'Andres', 'Fonseca', 'andresitofonseca13@gmail.com', 'pbkdf2:sha256:260000$SVET4Ak0LsenDeAO$ac4fd66d3232879c2e0a624cc003caa5c3b6cca185cfded5fdcf7d4a181394dc', '1053605316', 0),
(10, 'Juan', 'Hernandez', 'juan123@misena.edu.co', 'pbkdf2:sha256:260000$p9P7EyeWbbhvVQkQ$6e8d1b09c6dd28b594128bffa58b4649c514259becf6301cf335c66c8269e8ce', '2134454', 0),
(12, 'se', 'se', 'se@gmail.com', 'pbkdf2:sha256:260000$So05GxYnCPDioZAW$ab229a4753a0de093ad6c974c9cbbb88a339a1588cd9de085dc2ed7b0b9fe375', '22423454', 0),
(13, 'Santiago', 'Lombana', 'gordogonorrea@gmail.com', 'pbkdf2:sha256:260000$Qs0verlytyk1rAFn$a5cb9432b861141a7b76f09317468886328b12daf1868a44c180b36cce482a69', '1232135235', 0);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`ID`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `user`
--
ALTER TABLE `user`
  MODIFY `ID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
