# 🍳 KOOK · Kits de cocina con ingredientes pre-medidos

Aplicación web en la que el usuario elige una receta y recibe en casa un kit con los
ingredientes exactos para prepararla. Incluye tienda con carrito, gestión de pedidos y un
panel de administración completo.

Proyecto de 1º de DAM (CEAC FP Valencia) · Autor: [Ayman Mouzakki](https://github.com/aymanmzkk)

## Funcionalidades

**Usuarios**
- Registro e inicio de sesión con contraseñas cifradas (Werkzeug + Flask-Login)
- Catálogo de recetas y ficha de cada receta con ingredientes y pasos
- Carrito (añadir, cambiar cantidades, eliminar) y checkout con dirección de envío
- Perfil con el historial de pedidos
- Interfaz en español e inglés, con cambio de idioma en cualquier página

**Administración** (`/admin`)
- Panel con resumen de la tienda
- CRUD de recetas y de usuarios, y cambio de rol cliente/admin
- Listado de pedidos, detalle de cada uno y cambio de estado

## Tecnologías

| Capa | Tecnología |
| --- | --- |
| Backend | Python 3, Flask, Flask-Login |
| Base de datos | MySQL (9 tablas relacionadas: usuarios, recetas, ingredientes, pedidos…) |
| Frontend | Plantillas Jinja2, HTML5, CSS3, JavaScript |
| Servidor | Waitress (producción local) |

## Estructura

```
KOOK/
├── app.py                     # Rutas, lógica y traducciones ES/EN
├── templates/                 # Vistas Jinja2 (tienda y panel admin)
├── back-end/Bases de Datos/   # Script SQL de creación y datos de ejemplo
├── requirements.txt
├── .env.example               # Variables de configuración
└── start_waitress.bat         # Arranque con Waitress en Windows
```

## Cómo ejecutarlo

1. Instala MySQL (por ejemplo con XAMPP) y ejecuta el script
   `back-end/Bases de Datos/002-creacion de bases de datos.sql`.
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. (Opcional) Copia `.env.example` como `.env` y cambia los valores si tu MySQL no usa
   `root` sin contraseña.
4. Arranca la aplicación:
   ```bash
   python app.py
   ```
   y abre http://127.0.0.1:5000. En Windows también puedes usar `start_waitress.bat`
   (puerto 8000).

### Usuarios de demo

| Rol | Email | Contraseña |
| --- | --- | --- |
| Admin | admin@kook.com | admin123 |
| Cliente | juan@test.com | cliente123 |

## Lo que he aprendido

- Diseñar una base de datos relacional con tablas intermedias (recetas ↔ ingredientes, pedidos ↔ recetas)
- Gestionar sesiones, roles y rutas protegidas en Flask
- Separar la configuración sensible del código con variables de entorno
