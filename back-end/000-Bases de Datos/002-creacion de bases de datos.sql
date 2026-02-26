-- Crear base de datos
CREATE DATABASE KOOK;
USE KOOK;

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

-- Tabla categorias (para recetas)
CREATE TABLE categorias (
    categoria_id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL,
    descripcion TEXT
);

-- Tabla recetas
CREATE TABLE recetas (
    receta_id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    dificultad ENUM('facil', 'medio', 'dificil') DEFAULT 'medio',
    tiempo_preparacion INT, -- en minutos
    porciones INT DEFAULT 2,
    categoria_id INT,
    activa BOOLEAN DEFAULT TRUE,
    imagen_url VARCHAR(255),
    FOREIGN KEY (categoria_id) REFERENCES categorias(categoria_id)
);

-- Tabla ingredientes
CREATE TABLE ingredientes (
    ingrediente_id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    unidad VARCHAR(20) NOT NULL, -- gramos, ml, unidades, cucharadita, etc.
    stock DECIMAL(10,2) DEFAULT 0, -- opcional
    precio_compra DECIMAL(8,2) -- opcional
);

-- Tabla receta_ingredientes (relación con cantidad exacta)
CREATE TABLE receta_ingredientes (
    receta_id INT NOT NULL,
    ingrediente_id INT NOT NULL,
    cantidad DECIMAL(8,2) NOT NULL, -- cantidad exacta por receta
    PRIMARY KEY (receta_id, ingrediente_id),
    FOREIGN KEY (receta_id) REFERENCES recetas(receta_id) ON DELETE CASCADE,
    FOREIGN KEY (ingrediente_id) REFERENCES ingredientes(ingrediente_id) ON DELETE CASCADE
);

-- Tabla pasos_receta
CREATE TABLE pasos_receta (
    paso_id INT PRIMARY KEY AUTO_INCREMENT,
    receta_id INT NOT NULL,
    numero_paso INT NOT NULL,
    descripcion TEXT NOT NULL,
    imagen_paso VARCHAR(255),
    FOREIGN KEY (receta_id) REFERENCES recetas(receta_id) ON DELETE CASCADE
);

-- Tabla metodos_pago
CREATE TABLE metodos_pago (
    metodo_id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT NOT NULL,
    tipo ENUM('tarjeta', 'paypal', 'transferencia') NOT NULL,
    ultimos_digitos VARCHAR(4),
    token_seguro VARCHAR(255),
    predeterminado BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id) ON DELETE CASCADE
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
    instrucciones TEXT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id) ON DELETE CASCADE
);

-- Tabla detalles_pedido (relación pedido-receta con cantidad)
CREATE TABLE detalles_pedido (
    detalle_id INT PRIMARY KEY AUTO_INCREMENT,
    pedido_id INT NOT NULL,
    receta_id INT NOT NULL,
    cantidad INT NOT NULL DEFAULT 1,
    precio_unitario DECIMAL(8,2) NOT NULL,
    FOREIGN KEY (pedido_id) REFERENCES pedidos(pedido_id) ON DELETE CASCADE,
    FOREIGN KEY (receta_id) REFERENCES recetas(receta_id) ON DELETE CASCADE
);

-- ======================================================
-- INSERCIÓN DE DATOS DE EJEMPLO
-- ======================================================

-- Insertar categorías
INSERT INTO categorias (nombre, descripcion) VALUES
('Carne', 'Recetas con carne de res, cerdo, pollo, etc.'),
('Pescado', 'Recetas con pescados y mariscos'),
('Vegetariano', 'Recetas sin carne'),
('Vegano', 'Recetas sin productos de origen animal'),
('Postres', 'Dulces y postres'),
('Rápido', 'Comidas listas en menos de 30 minutos');

-- Insertar ingredientes
INSERT INTO ingredientes (nombre, unidad) VALUES
('Pechuga de pollo', 'g'),
('Arroz', 'g'),
('Aceite de oliva', 'ml'),
('Sal', 'g'),
('Pimienta', 'g'),
('Cebolla', 'unidad'),
('Ajo', 'diente'),
('Tomate', 'unidad'),
('Queso parmesano', 'g'),
('Nata líquida', 'ml'),
('Pasta', 'g'),
('Atún', 'lata'),
('Huevos', 'unidad'),
('Harina', 'g'),
('Azúcar', 'g'),
('Leche', 'ml');

-- Insertar recetas
INSERT INTO recetas (nombre, descripcion, dificultad, tiempo_preparacion, porciones, categoria_id, imagen_url) VALUES
('Pollo al curry', 'Delicioso pollo con salsa de curry y arroz', 'medio', 35, 2, 1, 'pollo_curry.jpg'),
('Risotto de champiñones', 'Cremoso risotto con champiñones y parmesano', 'medio', 40, 2, 3, 'risotto.jpg'),
('Tacos de pescado', 'Tacos estilo Baja con pescado empanizado', 'facil', 30, 2, 2, 'tacos_pescado.jpg'),
('Pasta carbonara', 'Pasta con salsa carbonara clásica', 'facil', 25, 2, 1, 'carbonara.jpg'),
('Ensalada César', 'Ensalada con pollo, lechuga y aderezo César', 'facil', 20, 2, 3, 'cesar.jpg');

-- Insertar receta_ingredientes (cantidades para 2 personas)
INSERT INTO receta_ingredientes (receta_id, ingrediente_id, cantidad) VALUES
(1, 1, 300),  -- pollo 300g
(1, 2, 200),  -- arroz 200g
(1, 3, 30),   -- aceite 30ml
(1, 4, 5),    -- sal 5g
(1, 5, 2),    -- pimienta 2g
(1, 6, 1),    -- cebolla 1 unidad
(1, 7, 2),    -- ajo 2 dientes
(2, 11, 250), -- pasta 250g
(2, 9, 50),   -- parmesano 50g
(2, 10, 100), -- nata 100ml
(2, 6, 1),    -- cebolla
(2, 7, 1),    -- ajo
(3, 12, 2),   -- atún 2 latas (simulando pescado)
(3, 13, 2),   -- huevos 2
(3, 14, 100), -- harina 100g
(3, 3, 50),   -- aceite 50ml
(4, 11, 250), -- pasta
(4, 13, 2),   -- huevos
(4, 9, 40),   -- queso
(4, 5, 2),    -- pimienta
(5, 1, 150),  -- pollo
(5, 8, 2),    -- tomate
(5, 4, 3),    -- sal
(5, 3, 20);   -- aceite

-- Insertar pasos_receta (para receta 1 como ejemplo)
INSERT INTO pasos_receta (receta_id, numero_paso, descripcion) VALUES
(1, 1, 'Picar la cebolla y los ajos finamente.'),
(1, 2, 'Cortar el pollo en dados y salpimentar.'),
(1, 3, 'Calentar aceite en una sartén y dorar el pollo. Retirar y reservar.'),
(1, 4, 'En la misma sartén, pochar la cebolla y el ajo.'),
(1, 5, 'Añadir el curry en polvo y remover.'),
(1, 6, 'Incorporar el pollo y la nata, cocinar 10 minutos.'),
(1, 7, 'Servir con arroz blanco.');

-- Insertar usuarios de ejemplo
INSERT INTO usuarios (nombre, apellidos, telefono, direccion, correo_electronico, pais, contrasenya, tipo_usuario) VALUES
('Ana', 'García López', '+34 600 111 222', 'Calle Mayor 10, Madrid', 'ana.garcia@email.com', 'España', '12345678', 'cliente'),
('Carlos', 'Rodríguez Pérez', '+34 611 222 333', 'Av. Diagonal 25, Barcelona', 'carlos.rodriguez@email.com', 'España', '12345678', 'cliente'),
('Laura', 'Martínez Sánchez', '+34 622 333 444', 'Calle Gran Vía 45, Valencia', 'laura.martinez@email.com', 'España', '12345678', 'cliente'),
('Admin', 'KOOK', '+34 600 000 000', 'Calle Falsa 123', 'admin@kook.com', 'España', 'admin123', 'admin');

-- Insertar métodos de pago
INSERT INTO metodos_pago (usuario_id, tipo, ultimos_digitos, predeterminado) VALUES
(1, 'tarjeta', '1234', TRUE),
(2, 'paypal', NULL, TRUE),
(3, 'tarjeta', '5678', TRUE);

-- Insertar pedidos
INSERT INTO pedidos (usuario_id, fecha_entrega, estado, total, direccion_envio) VALUES
(1, '2026-03-10', 'entregado', 29.98, 'Calle Mayor 10, Madrid'),
(2, '2026-03-12', 'enviado', 14.99, 'Av. Diagonal 25, Barcelona'),
(3, '2026-03-15', 'pendiente', 12.99, 'Calle Gran Vía 45, Valencia');

-- Insertar detalles_pedido
INSERT INTO detalles_pedido (pedido_id, receta_id, cantidad, precio_unitario) VALUES
(1, 1, 1, 14.99),
(1, 2, 1, 14.99),
(2, 3, 1, 14.99),
(3, 4, 1, 12.99);

-- ======================================================
-- CREACIÓN DE USUARIO PARA LA APLICACIÓN
-- ======================================================
CREATE USER 'usuario-kook'@'localhost' IDENTIFIED BY 'Kook2026$';

GRANT USAGE ON *.* TO 'usuario-kook'@'localhost';
GRANT ALL PRIVILEGES ON KOOK.* TO 'usuario-kook'@'localhost';

FLUSH PRIVILEGES;

-- ======================================================
-- ÍNDICES PARA MEJORAR RENDIMIENTO
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
-- VISTAS ÚTILES
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

-- Vista de recetas con ingredientes y categoría
CREATE VIEW vista_recetas_completa AS
SELECT 
    r.receta_id,
    r.nombre AS receta,
    r.descripcion,
    r.dificultad,
    r.tiempo_preparacion,
    r.porciones,
    c.nombre AS categoria,
    GROUP_CONCAT(CONCAT(i.nombre, ': ', ri.cantidad, ' ', i.unidad) SEPARATOR '; ') AS ingredientes
FROM recetas r
JOIN categorias c ON r.categoria_id = c.categoria_id
LEFT JOIN receta_ingredientes ri ON r.receta_id = ri.receta_id
LEFT JOIN ingredientes i ON ri.ingrediente_id = i.ingrediente_id
GROUP BY r.receta_id;

-- Vista de pedidos recientes (últimos 30 días)
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

-- Vista de recetas más populares (basado en número de veces pedidas)
CREATE VIEW vista_recetas_populares AS
SELECT 
    r.receta_id,
    r.nombre AS receta,
    COUNT(dp.detalle_id) AS veces_pedida
FROM recetas r
LEFT JOIN detalles_pedido dp ON r.receta_id = dp.receta_id
GROUP BY r.receta_id
ORDER BY veces_pedida DESC;