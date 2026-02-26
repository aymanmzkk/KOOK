KOOK - Esquema de Base de Datos
TABLAS CREADAS

Tablas principales
usuarios – Almacena la información de los clientes registrados.
recetas – Catálogo de recetas disponibles.
ingredientes – Lista de todos los ingredientes que se pueden usar.
categorias – Clasificación de las recetas (ej. carne, pescado, vegetariano, postre).
pedidos – Órdenes de compra realizadas por los usuarios.
metodos_pago – Formas de pago asociadas a cada usuario.

Tablas de relación y detalles
receta_ingredientes – Relaciona recetas con ingredientes y especifica la cantidad exacta.
pasos_receta – Pasos detallados para preparar cada receta.
detalles_pedido – Recetas incluidas en cada pedido (cantidad y precio).

Tablas opcionales (para futura expansión)
inventario – Control de stock de ingredientes.
proveedores – Información de proveedores.
compras – Registro de compras a proveedores.
compra_detalles – Detalle de cada compra.

RELACIONES ENTRE TABLAS
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