-- Crear base de datos
CREATE DATABASE KOOK;
USE KOOK;

-- ======================================================
-- TABLAS PRINCIPALES
-- ======================================================

-- Tabla usuarios
CREATE TABLE usuarios (
    usuario_id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    telefono VARCHAR(20),
    direccion VARCHAR(255),
    correo_electronico VARCHAR(150) UNIQUE NOT NULL,
    pais VARCHAR(50),
    contrasenya VARCHAR(255) NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tipo_usuario ENUM('admin', 'cliente') DEFAULT 'cliente'
);

-- Tabla categorias
CREATE TABLE categorias (
    categoria_id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL
);

-- Tabla recetas
CREATE TABLE recetas (
    receta_id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    dificultad VARCHAR(20) DEFAULT 'medio',
    tiempo_preparacion INT,
    porciones INT DEFAULT 2,
    categoria_id INT,
    activa BOOLEAN DEFAULT TRUE,
    precio_venta DECIMAL(8,2) DEFAULT 14.99,
    FOREIGN KEY (categoria_id) REFERENCES categorias(categoria_id) ON DELETE SET NULL
);

-- Tabla ingredientes (con soporte multi-idioma)
CREATE TABLE ingredientes (
    ingrediente_id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    nombre_en VARCHAR(100),
    unidad VARCHAR(20) NOT NULL,
    stock DECIMAL(10,2) DEFAULT 0
);

-- Tabla receta_ingredientes
CREATE TABLE receta_ingredientes (
    receta_id INT NOT NULL,
    ingrediente_id INT NOT NULL,
    cantidad DECIMAL(8,2) NOT NULL,
    PRIMARY KEY (receta_id, ingrediente_id),
    FOREIGN KEY (receta_id) REFERENCES recetas(receta_id) ON DELETE CASCADE,
    FOREIGN KEY (ingrediente_id) REFERENCES ingredientes(ingrediente_id) ON DELETE CASCADE
);

-- Tabla pasos_receta (con soporte multi-idioma)
CREATE TABLE pasos_receta (
    paso_id INT PRIMARY KEY AUTO_INCREMENT,
    receta_id INT NOT NULL,
    numero_paso INT NOT NULL,
    descripcion TEXT NOT NULL,
    descripcion_en TEXT,
    FOREIGN KEY (receta_id) REFERENCES recetas(receta_id) ON DELETE CASCADE
);

-- Tabla pedidos
CREATE TABLE pedidos (
    pedido_id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT NOT NULL,
    fecha_pedido DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_entrega DATE,
    estado ENUM('pendiente', 'preparando', 'enviado', 'entregado', 'cancelado') DEFAULT 'pendiente',
    total DECIMAL(10,2) NOT NULL,
    direccion_envio TEXT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id) ON DELETE CASCADE
);

-- Tabla detalles_pedido
CREATE TABLE detalles_pedido (
    detalle_id INT PRIMARY KEY AUTO_INCREMENT,
    pedido_id INT NOT NULL,
    receta_id INT NOT NULL,
    cantidad INT NOT NULL DEFAULT 1,
    precio_unitario DECIMAL(8,2) NOT NULL,
    FOREIGN KEY (pedido_id) REFERENCES pedidos(pedido_id) ON DELETE CASCADE,
    FOREIGN KEY (receta_id) REFERENCES recetas(receta_id) ON DELETE CASCADE
);

-- Tabla metodos_pago (opcional)
CREATE TABLE metodos_pago (
    metodo_id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT NOT NULL,
    tipo ENUM('tarjeta', 'paypal', 'transferencia') NOT NULL,
    ultimos_digitos VARCHAR(4),
    predeterminado BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id) ON DELETE CASCADE
);

-- ======================================================
-- DATOS DE EJEMPLO
-- ======================================================

-- Insertar categorías
INSERT INTO categorias (nombre) VALUES 
('Carne'), 
('Pescado'), 
('Vegetariano'), 
('Postres'), 
('Rápido');

-- Insertar ingredientes con traducciones
INSERT INTO ingredientes (nombre, nombre_en, unidad) VALUES
('Pechuga de pollo', 'Chicken breast', 'g'),
('Arroz', 'Rice', 'g'),
('Aceite de oliva', 'Olive oil', 'ml'),
('Sal', 'Salt', 'g'),
('Pimienta', 'Pepper', 'g'),
('Cebolla', 'Onion', 'unidad'),
('Ajo', 'Garlic', 'diente'),
('Tomate', 'Tomato', 'unidad'),
('Queso parmesano', 'Parmesan cheese', 'g'),
('Nata líquida', 'Heavy cream', 'ml'),
('Pasta', 'Pasta', 'g'),
('Huevos', 'Eggs', 'unidad'),
('Harina', 'Flour', 'g'),
('Champiñones', 'Mushrooms', 'g'),
('Curry', 'Curry', 'cucharadita');

-- Insertar recetas
INSERT INTO recetas (nombre, descripcion, dificultad, tiempo_preparacion, porciones, categoria_id, precio_venta) VALUES
('Pollo al Curry', 'Delicioso pollo con salsa de curry y arroz', 'medio', 35, 2, 1, 14.99),
('Risotto de Champiñones', 'Cremoso risotto con champiñones y parmesano', 'medio', 40, 2, 3, 12.99),
('Tacos de Pescado', 'Tacos estilo Baja con pescado empanizado', 'facil', 30, 2, 2, 13.99),
('Pasta Carbonara', 'Pasta con salsa carbonara clásica', 'facil', 25, 2, 1, 11.99),
('Ensalada César', 'Ensalada con pollo, lechuga y aderezo César', 'facil', 20, 2, 3, 9.99);

-- Insertar receta_ingredientes
INSERT INTO receta_ingredientes (receta_id, ingrediente_id, cantidad) VALUES
-- Pollo al Curry
(1, 1, 300), (1, 2, 200), (1, 3, 30), (1, 4, 5), (1, 5, 2), (1, 6, 1), (1, 7, 2), (1, 15, 10),
-- Risotto
(2, 2, 250), (2, 9, 50), (2, 10, 100), (2, 6, 1), (2, 7, 1), (2, 14, 200),
-- Tacos
(3, 12, 2), (3, 13, 100), (3, 3, 50), (3, 4, 3),
-- Carbonara
(4, 11, 250), (4, 12, 2), (4, 9, 40), (4, 5, 2),
-- Ensalada César
(5, 1, 150), (5, 8, 2), (5, 4, 3), (5, 3, 20);

-- Insertar pasos_receta con traducciones
INSERT INTO pasos_receta (receta_id, numero_paso, descripcion, descripcion_en) VALUES
-- Pollo al Curry
(1, 1, 'Picar la cebolla y los ajos finamente.', 'Finely chop the onion and garlic.'),
(1, 2, 'Cortar el pollo en dados y salpimentar.', 'Cut the chicken into cubes and season.'),
(1, 3, 'Calentar aceite y dorar el pollo. Reservar.', 'Heat oil and brown the chicken. Set aside.'),
(1, 4, 'Sofreír la cebolla y el ajo.', 'Sauté the onion and garlic.'),
(1, 5, 'Añadir el curry y la nata, cocinar 10 minutos.', 'Add curry and cream, cook for 10 minutes.'),
(1, 6, 'Servir con arroz blanco.', 'Serve with white rice.'),
-- Risotto
(2, 1, 'Picar la cebolla y el ajo.', 'Chop the onion and garlic.'),
(2, 2, 'Sofreír en aceite.', 'Sauté in oil.'),
(2, 3, 'Añadir el arroz y rehogar.', 'Add rice and toast.'),
(2, 4, 'Añadir caldo poco a poco.', 'Add broth gradually.'),
(2, 5, 'Añadir champiñones y queso.', 'Add mushrooms and cheese.'),
(2, 6, 'Servir caliente.', 'Serve hot.'),
-- Tacos
(3, 1, 'Pasar el pescado por harina y huevo.', 'Coat fish with flour and egg.'),
(3, 2, 'Freír en aceite caliente.', 'Fry in hot oil.'),
(3, 3, 'Calentar las tortillas.', 'Warm the tortillas.'),
(3, 4, 'Servir con repollo y salsa.', 'Serve with cabbage and sauce.');

-- Insertar usuarios (contraseñas: admin123, ayman2004, cliente123)
INSERT INTO usuarios (nombre, apellidos, correo_electronico, telefono, direccion, pais, contrasenya, tipo_usuario) VALUES
('Admin', 'KOOK', 'admin@kook.com', '+34 600 000 000', 'Calle Admin 1', 'España', 'scrypt:32768:8:1$gJxGqsp37GLCF8BZ$8e04be5fdff9df4994e2878e22d1dd0d3fb83578430a75a7f7ec89de355d0a4318b2e1bfe42a3a5fea3f9dffddcbcf91daf0ee199384c23515a9f10788c3b210', 'admin'),
('Ayman', 'Mouzakki', 'ayman@kook.com', '+34 600 111 222', 'Calle Ayman 123', 'España', 'scrypt:32768:8:1$Fo6uawfuKUuoVHqX$aa5fe1a24b0a98124bd92f5c586cb2eaa0892f0f98aaba3570013be64cfd09d0192b1587f463ecfdef662b77bf647cdb981fe8e866dbaae855d2d21adfcdfded', 'admin'),
('Juan', 'Pérez', 'juan@test.com', '+34 611 111 111', 'Calle Mayor 1', 'España', 'scrypt:32768:8:1$gJxGqsp37GLCF8BZ$8e04be5fdff9df4994e2878e22d1dd0d3fb83578430a75a7f7ec89de355d0a4318b2e1bfe42a3a5fea3f9dffddcbcf91daf0ee199384c23515a9f10788c3b210', 'cliente'),
('María', 'López', 'maria@test.com', '+34 622 222 222', 'Av. Diagonal 2', 'España', 'scrypt:32768:8:1$gJxGqsp37GLCF8BZ$8e04be5fdff9df4994e2878e22d1dd0d3fb83578430a75a7f7ec89de355d0a4318b2e1bfe42a3a5fea3f9dffddcbcf91daf0ee199384c23515a9f10788c3b210', 'cliente');

-- Insertar pedidos de ejemplo
INSERT INTO pedidos (usuario_id, fecha_entrega, estado, total, direccion_envio) VALUES
(3, DATE_ADD(CURDATE(), INTERVAL 2 DAY), 'pendiente', 14.99, 'Calle Mayor 1, Madrid'),
(3, DATE_ADD(CURDATE(), INTERVAL 1 DAY), 'enviado', 12.99, 'Calle Mayor 1, Madrid'),
(4, CURDATE(), 'entregado', 27.98, 'Av. Diagonal 2, Barcelona');

-- Insertar detalles de pedidos
INSERT INTO detalles_pedido (pedido_id, receta_id, cantidad, precio_unitario) VALUES
(1, 1, 1, 14.99),
(2, 2, 1, 12.99),
(3, 1, 1, 14.99),
(3, 3, 1, 12.99);

-- ======================================================
-- CREACIÓN DE USUARIO PARA LA APLICACIÓN
-- ======================================================
CREATE USER IF NOT EXISTS 'usuario-kook'@'localhost' IDENTIFIED BY 'Kook2026$';
GRANT ALL PRIVILEGES ON KOOK.* TO 'usuario-kook'@'localhost';
FLUSH PRIVILEGES;

-- ======================================================
-- ÍNDICES
-- ======================================================
CREATE INDEX idx_usuarios_email ON usuarios(correo_electronico);
CREATE INDEX idx_usuarios_nombre ON usuarios(nombre, apellidos);
CREATE INDEX idx_recetas_nombre ON recetas(nombre);
CREATE INDEX idx_recetas_categoria ON recetas(categoria_id);
CREATE INDEX idx_pedidos_usuario ON pedidos(usuario_id);
CREATE INDEX idx_pedidos_fecha ON pedidos(fecha_pedido);
CREATE INDEX idx_detalles_pedido_pedido ON detalles_pedido(pedido_id);
CREATE INDEX idx_detalles_pedido_receta ON detalles_pedido(receta_id);
CREATE INDEX idx_receta_ingredientes_receta ON receta_ingredientes(receta_id);
CREATE INDEX idx_receta_ingredientes_ingrediente ON receta_ingredientes(ingrediente_id);

-- ======================================================
-- VISTAS
-- ======================================================

-- Vista de pedidos con información del usuario
CREATE VIEW vista_pedidos_usuario AS
SELECT 
    p.pedido_id,
    p.fecha_pedido,
    p.estado,
    p.total,
    u.usuario_id,
    u.nombre,
    u.apellidos,
    u.correo_electronico
FROM pedidos p
JOIN usuarios u ON p.usuario_id = u.usuario_id;

-- Vista de recetas con ingredientes
CREATE VIEW vista_recetas_completa AS
SELECT 
    r.receta_id,
    r.nombre,
    r.descripcion,
    r.dificultad,
    r.tiempo_preparacion,
    r.porciones,
    r.precio_venta,
    c.nombre AS categoria,
    GROUP_CONCAT(CONCAT(i.nombre, ': ', ri.cantidad, ' ', i.unidad) SEPARATOR '; ') AS ingredientes
FROM recetas r
JOIN categorias c ON r.categoria_id = c.categoria_id
LEFT JOIN receta_ingredientes ri ON r.receta_id = ri.receta_id
LEFT JOIN ingredientes i ON ri.ingrediente_id = i.ingrediente_id
GROUP BY r.receta_id;

-- Vista de pedidos recientes
CREATE VIEW vista_pedidos_recientes AS
SELECT 
    p.pedido_id,
    p.fecha_pedido,
    p.estado,
    p.total,
    u.nombre,
    u.apellidos
FROM pedidos p
JOIN usuarios u ON p.usuario_id = u.usuario_id
WHERE p.fecha_pedido >= CURDATE() - INTERVAL 30 DAY
ORDER BY p.fecha_pedido DESC;

-- Vista de recetas más populares
CREATE VIEW vista_recetas_populares AS
SELECT 
    r.receta_id,
    r.nombre,
    COUNT(dp.detalle_id) AS veces_pedida
FROM recetas r
LEFT JOIN detalles_pedido dp ON r.receta_id = dp.receta_id
GROUP BY r.receta_id
ORDER BY veces_pedida DESC;