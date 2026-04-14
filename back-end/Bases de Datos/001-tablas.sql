KOOK - Esquema de Base de Datos

TABLAS CREADAS
Tablas principales
usuarios – Almacena la información de los clientes registrados (nombre, apellidos, email, teléfono, dirección, país, contraseña hasheada, tipo_usuario, fecha_registro).

recetas – Catálogo de recetas disponibles (nombre, descripción, dificultad, tiempo_preparacion, porciones, categoria_id, precio_venta, activa).

ingredientes – Lista de todos los ingredientes que se pueden usar (nombre, nombre_en para inglés, unidad, stock).

categorias – Clasificación de las recetas (carne, pescado, vegetariano, postres).

pedidos – Órdenes de compra realizadas por los usuarios (usuario_id, fecha_pedido, fecha_entrega, estado, total, direccion_envio).

metodos_pago – Formas de pago asociadas a cada usuario (tipo, últimos dígitos, predeterminado).

Tablas de relación y detalles
receta_ingredientes – Relaciona recetas con ingredientes y especifica la cantidad exacta (receta_id, ingrediente_id, cantidad).

pasos_receta – Pasos detallados para preparar cada receta (receta_id, numero_paso, descripcion, descripcion_en para inglés).

detalles_pedido – Recetas incluidas en cada pedido (pedido_id, receta_id, cantidad, precio_unitario).

Tablas opcionales (para futura expansión)
inventario – Control de stock de ingredientes.

proveedores – Información de proveedores.

compras – Registro de compras a proveedores.

compra_detalles – Detalle de cada compra.

RELACIONES ENTRE TABLAS:
usuarios (1) ──< (N) pedidos
usuarios (1) ──< (N) metodos_pago
recetas (1) ──< (N) receta_ingredientes ──> (1) ingredientes
recetas (1) ──< (N) pasos_receta
recetas (1) ──< (N) detalles_pedido ──> (1) pedidos
categorias (1) ──< (N) recetas
ÍNDICES CREADOS
Índices para búsquedas frecuentes:
idx_usuarios_email (email) – Búsqueda rápida por email en login.

idx_usuarios_nombre (nombre, apellidos) – Búsqueda de usuarios.

idx_recetas_nombre (nombre) – Búsqueda de recetas por nombre.

idx_recetas_categoria (id_categoria) – Filtrado por categoría.

idx_pedidos_usuario (id_usuario) – Historial de pedidos de un usuario.

idx_pedidos_fecha (fecha_pedido) – Consultas por fecha.

Índices para relaciones:
idx_receta_ingredientes_receta (id_receta)

idx_receta_ingredientes_ingrediente (id_ingrediente)

idx_detalles_pedido_pedido (id_pedido)

idx_detalles_pedido_receta (id_receta)

VISTAS CREADAS
vista_pedidos_recientes – Muestra los últimos pedidos con datos de usuario y total.

vista_recetas_populares – Recetas más pedidas (basado en detalles_pedido).

vista_ingredientes_por_receta – Desglose de ingredientes para cada receta.

vista_stock_critico – Ingredientes con stock bajo (si se implementa inventario).

SQL DE CREACIÓN DE TABLAS:
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
    FOREIGN KEY (categoria_id) REFERENCES categorias(categoria_id)
);

-- Tabla ingredientes
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

-- Tabla pasos_receta
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

-- Tabla metodos_pago
CREATE TABLE metodos_pago (
    metodo_id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT NOT NULL,
    tipo ENUM('tarjeta', 'paypal', 'transferencia') NOT NULL,
    ultimos_digitos VARCHAR(4),
    predeterminado BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id) ON DELETE CASCADE
);
DATOS DE EJEMPLO
sql
-- Categorías
INSERT INTO categorias (nombre) VALUES ('Carne'), ('Pescado'), ('Vegetariano'), ('Postres');

-- Recetas
INSERT INTO recetas (nombre, descripcion, dificultad, tiempo_preparacion, porciones, categoria_id, precio_venta) VALUES
('Pollo al Curry', 'Delicioso pollo con salsa de curry', 'medio', 35, 2, 1, 14.99),
('Risotto de Champiñones', 'Cremoso risotto con champiñones', 'medio', 40, 2, 3, 12.99),
('Tacos de Pescado', 'Tacos estilo Baja', 'facil', 30, 2, 2, 13.99);

-- Ingredientes
INSERT INTO ingredientes (nombre, nombre_en, unidad) VALUES
('Pechuga de pollo', 'Chicken breast', 'g'),
('Arroz', 'Rice', 'g'),
('Aceite de oliva', 'Olive oil', 'ml'),
('Sal', 'Salt', 'g'),
('Cebolla', 'Onion', 'unidad'),
('Ajo', 'Garlic', 'diente');

-- Usuarios
INSERT INTO usuarios (nombre, apellidos, correo_electronico, contrasenya, tipo_usuario) VALUES
('Admin', 'KOOK', 'admin@kook.com', 'admin123', 'admin'),
('Ayman', 'Mouzakki', 'ayman@kook.com', 'ayman2004', 'admin');
CREDENCIALES DE ACCESO
Usuario	Email	Contraseña	Tipo
Usuario Prueba	usuario@kook.com	usuario123	Usuario
Ayman Mouzakki	ayman@kook.com	ayman2004	Admin