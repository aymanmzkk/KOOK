from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
import os
import json

# Configuración de templates
template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=template_dir)
app.secret_key = 'clave-secreta-koook-2026'
app.permanent_session_lifetime = timedelta(days=7)

# Configuración BD
db_config = {
    'host': 'localhost',
    'user': 'usuario-kook',
    'password': 'Kook2026$',
    'database': 'KOOK',
    'port': 3306    
}

# ======================================================
# TRADUCCIONES DIRECTAS
# ======================================================

TRADUCCIONES = {
    'es': {
        'inicio': 'Inicio',
        'recetas': 'Recetas',
        'como_funciona': 'Cómo funciona',
        'contacto': 'Contacto',
        'perfil': 'Mi Perfil',
        'carrito': 'Carrito',
        'admin': 'Admin',
        'login': 'Iniciar Sesión',
        'registro': 'Regístrate',
        'logout': 'Cerrar Sesión',
        'saludo': 'Hola',
        'footer_descripcion': 'Cocina sin errores con ingredientes pre-medidos.',
        'footer_enlaces': 'Enlaces',
        'footer_contacto': 'Contacto',
        'footer_derechos': 'Todos los derechos reservados.',
        'footer_proyecto': 'Proyecto educativo DAM/DAW.',
        'home_titulo': 'Cocina como un chef con medidas perfectas',
        'home_subtitulo': 'KOOK te envía todos los ingredientes pre-medidos. Todo incluido, hasta la última pizca de sal.',
        'home_ver_recetas': 'Ver recetas',
        'home_como_funciona': 'Cómo funciona',
        'home_por_que': '¿Por qué elegir KOOK?',
        'home_descripcion': 'La única app que elimina las adivinanzas de la cocina',
        'home_ingredientes_titulo': 'Ingredientes Pre-Medidos',
        'home_ingredientes_texto': 'Cada ingrediente viene en la cantidad exacta.',
        'home_desperdicio_titulo': 'Cero Desperdicio',
        'home_desperdicio_texto': 'Solo recibes lo que necesitas.',
        'home_instrucciones_titulo': 'Instrucciones Infalibles',
        'home_instrucciones_texto': 'Pasos detallados, perfecto para principiantes.',
        'home_entrega_titulo': 'Entrega a Domicilio',
        'home_entrega_texto': 'Recibe tu KOOK Box fresca en casa.',
        'home_cta_titulo': '¿Listo para cocinar sin errores?',
        'home_cta_texto': 'Únete a miles de personas que ya cocinan como chefs.',
        'home_cta_boton': 'Empieza ahora',
        'recetas_titulo': 'Nuestras Recetas',
        'recetas_ver_detalles': 'Ver detalles',
        'recetas_anadir': 'Añadir',
        'recetas_sin_recetas': 'No hay recetas disponibles',
        'recetas_sin_recetas_texto': 'Pronto añadiremos nuevas recetas para ti.',
        'detalle_tiempo': 'Tiempo',
        'detalle_minutos': 'minutos',
        'detalle_porciones': 'porciones',
        'detalle_dificultad': 'Dificultad',
        'detalle_categoria': 'Categoría',
        'detalle_precio': 'Precio',
        'detalle_ingredientes': 'Ingredientes',
        'detalle_preparacion': 'Preparación',
        'detalle_paso': 'Paso',
        'detalle_anadir_carrito': 'Añadir al carrito',
        'detalle_volver': 'Volver a recetas',
        'detalle_sin_ingredientes': 'No hay ingredientes disponibles',
        'detalle_sin_pasos': 'No hay pasos disponibles',
        'carrito_titulo': 'Tu carrito',
        'carrito_vacio': 'Tu carrito está vacío',
        'carrito_vacio_texto': 'Explora nuestras recetas y añade las que más te gusten.',
        'carrito_ver_recetas': 'Ver recetas',
        'carrito_receta': 'Receta',
        'carrito_precio': 'Precio',
        'carrito_cantidad': 'Cantidad',
        'carrito_subtotal': 'Subtotal',
        'carrito_total': 'Total',
        'carrito_gastos_envio': 'Gastos de envío',
        'carrito_proceder': 'Proceder al pago',
        'carrito_seguir': 'Seguir comprando',
        'carrito_eliminar': 'Eliminar',
        'checkout_titulo': 'Finalizar Compra',
        'checkout_resumen': 'Resumen del pedido',
        'checkout_datos_envio': 'Datos de envío',
        'checkout_direccion': 'Dirección de entrega',
        'checkout_terminos': 'Acepto los términos y condiciones',
        'checkout_confirmar': 'Confirmar pedido',
        'checkout_volver': 'Volver al carrito',
        'login_titulo': 'Iniciar Sesión',
        'login_email': 'Email',
        'login_password': 'Contraseña',
        'login_entrar': 'Entrar',
        'login_no_cuenta': '¿No tienes cuenta?',
        'login_registrate': 'Regístrate',
        'registro_titulo': 'Crear Cuenta',
        'registro_nombre': 'Nombre',
        'registro_apellidos': 'Apellidos',
        'registro_email': 'Email',
        'registro_telefono': 'Teléfono',
        'registro_direccion': 'Dirección',
        'registro_password': 'Contraseña',
        'registro_confirm_password': 'Confirmar Contraseña',
        'registro_acepto': 'Acepto la política de privacidad',
        'registro_boton': 'Registrarse',
        'registro_ya_tienes_cuenta': '¿Ya tienes cuenta?',
        'registro_inicia_sesion': 'Inicia sesión',
        'perfil_titulo': 'Mi Perfil',
        'perfil_informacion': 'Información personal',
        'perfil_telefono': 'Teléfono',
        'perfil_direccion': 'Dirección',
        'perfil_pais': 'País',
        'perfil_miembro_desde': 'Miembro desde',
        'perfil_estadisticas': 'Estadísticas',
        'perfil_pedidos_realizados': 'Pedidos realizados',
        'perfil_tipo_usuario': 'Tipo de usuario',
        'perfil_ultimos_pedidos': 'Últimos pedidos',
        'perfil_fecha': 'Fecha',
        'perfil_total': 'Total',
        'perfil_estado': 'Estado',
        'perfil_sin_pedidos': 'No tienes pedidos aún',
        'perfil_explora_recetas': '¡Explora nuestras recetas!',
        'perfil_ver_recetas': 'Ver recetas',
        'perfil_cerrar_sesion': 'Cerrar sesión',
        'admin_dashboard': 'Panel de Administración',
        'admin_usuarios': 'Usuarios',
        'admin_recetas': 'Recetas',
        'admin_pedidos': 'Pedidos',
        'admin_pendientes': 'Pendientes',
        'admin_acciones_rapidas': 'Acciones rápidas',
        'admin_gestionar_recetas': 'Gestionar Recetas',
        'admin_gestionar_usuarios': 'Gestionar Usuarios',
        'admin_ver_pedidos': 'Ver Pedidos',
        'admin_nueva_receta': 'Nueva Receta',
        'mensaje': 'Mensaje'
    },
    'en': {
        'inicio': 'Home',
        'recetas': 'Recipes',
        'como_funciona': 'How it works',
        'contacto': 'Contact',
        'perfil': 'My Profile',
        'carrito': 'Cart',
        'admin': 'Admin',
        'login': 'Login',
        'registro': 'Sign Up',
        'logout': 'Logout',
        'saludo': 'Hello',
        'footer_descripcion': 'Cook without mistakes with pre-measured ingredients.',
        'footer_enlaces': 'Links',
        'footer_contacto': 'Contact',
        'footer_derechos': 'All rights reserved.',
        'footer_proyecto': 'Educational project DAM/DAW.',
        'home_titulo': 'Cook like a chef with perfect measurements',
        'home_subtitulo': 'KOOK sends you all pre-measured ingredients. Everything included, down to the last pinch of salt.',
        'home_ver_recetas': 'View recipes',
        'home_como_funciona': 'How it works',
        'home_por_que': 'Why choose KOOK?',
        'home_descripcion': 'The only app that eliminates kitchen guesswork',
        'home_ingredientes_titulo': 'Pre-Measured Ingredients',
        'home_ingredientes_texto': 'Each ingredient comes in the exact amount.',
        'home_desperdicio_titulo': 'Zero Waste',
        'home_desperdicio_texto': 'You only receive what you need.',
        'home_instrucciones_titulo': 'Foolproof Instructions',
        'home_instrucciones_texto': 'Detailed steps, perfect for beginners.',
        'home_entrega_titulo': 'Home Delivery',
        'home_entrega_texto': 'Receive your fresh KOOK Box at home.',
        'home_cta_titulo': 'Ready to cook without mistakes?',
        'home_cta_texto': 'Join thousands of people already cooking like chefs.',
        'home_cta_boton': 'Start now',
        'recetas_titulo': 'Our Recipes',
        'recetas_ver_detalles': 'View details',
        'recetas_anadir': 'Add',
        'recetas_sin_recetas': 'No recipes available',
        'recetas_sin_recetas_texto': 'We will add new recipes soon.',
        'detalle_tiempo': 'Time',
        'detalle_minutos': 'minutes',
        'detalle_porciones': 'servings',
        'detalle_dificultad': 'Difficulty',
        'detalle_categoria': 'Category',
        'detalle_precio': 'Price',
        'detalle_ingredientes': 'Ingredients',
        'detalle_preparacion': 'Preparation',
        'detalle_paso': 'Step',
        'detalle_anadir_carrito': 'Add to cart',
        'detalle_volver': 'Back to recipes',
        'detalle_sin_ingredientes': 'No ingredients available',
        'detalle_sin_pasos': 'No steps available',
        'carrito_titulo': 'Your cart',
        'carrito_vacio': 'Your cart is empty',
        'carrito_vacio_texto': 'Explore our recipes and add your favorites.',
        'carrito_ver_recetas': 'View recipes',
        'carrito_receta': 'Recipe',
        'carrito_precio': 'Price',
        'carrito_cantidad': 'Quantity',
        'carrito_subtotal': 'Subtotal',
        'carrito_total': 'Total',
        'carrito_gastos_envio': 'Shipping costs',
        'carrito_proceder': 'Proceed to checkout',
        'carrito_seguir': 'Continue shopping',
        'carrito_eliminar': 'Delete',
        'checkout_titulo': 'Checkout',
        'checkout_resumen': 'Order summary',
        'checkout_datos_envio': 'Shipping details',
        'checkout_direccion': 'Delivery address',
        'checkout_terminos': 'I accept the terms and conditions',
        'checkout_confirmar': 'Confirm order',
        'checkout_volver': 'Back to cart',
        'login_titulo': 'Login',
        'login_email': 'Email',
        'login_password': 'Password',
        'login_entrar': 'Sign in',
        'login_no_cuenta': 'Don\'t have an account?',
        'login_registrate': 'Sign up',
        'registro_titulo': 'Create Account',
        'registro_nombre': 'First name',
        'registro_apellidos': 'Last name',
        'registro_email': 'Email',
        'registro_telefono': 'Phone',
        'registro_direccion': 'Address',
        'registro_password': 'Password',
        'registro_confirm_password': 'Confirm Password',
        'registro_acepto': 'I accept the privacy policy',
        'registro_boton': 'Register',
        'registro_ya_tienes_cuenta': 'Already have an account?',
        'registro_inicia_sesion': 'Login',
        'perfil_titulo': 'My Profile',
        'perfil_informacion': 'Personal information',
        'perfil_telefono': 'Phone',
        'perfil_direccion': 'Address',
        'perfil_pais': 'Country',
        'perfil_miembro_desde': 'Member since',
        'perfil_estadisticas': 'Statistics',
        'perfil_pedidos_realizados': 'Orders placed',
        'perfil_tipo_usuario': 'User type',
        'perfil_ultimos_pedidos': 'Recent orders',
        'perfil_fecha': 'Date',
        'perfil_total': 'Total',
        'perfil_estado': 'Status',
        'perfil_sin_pedidos': 'You have no orders yet',
        'perfil_explora_recetas': 'Explore our recipes!',
        'perfil_ver_recetas': 'View recipes',
        'perfil_cerrar_sesion': 'Logout',
        'admin_dashboard': 'Administration Panel',
        'admin_usuarios': 'Users',
        'admin_recetas': 'Recipes',
        'admin_pedidos': 'Orders',
        'admin_pendientes': 'Pending',
        'admin_acciones_rapidas': 'Quick actions',
        'admin_gestionar_recetas': 'Manage Recipes',
        'admin_gestionar_usuarios': 'Manage Users',
        'admin_ver_pedidos': 'View Orders',
        'admin_nueva_receta': 'New Recipe',
        'mensaje': 'Message'
    }
}

def load_translations(lang='es'):
    return TRADUCCIONES.get(lang, TRADUCCIONES['es'])

@app.route('/change-language/<lang>')
def change_language(lang):
    if lang in ['es', 'en']:
        session['language'] = lang
        flash(f'Idioma cambiado a {lang}', 'success')
    return redirect(request.referrer or url_for('home'))

# ======================================================
# FUNCIONES BD
# ======================================================

def get_connection():
    return mysql.connector.connect(**db_config)

def registrar_usuario(nombre, apellidos, email, telefono, direccion, password):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        password_hash = generate_password_hash(password)
        sql = """INSERT INTO usuarios (nombre, apellidos, correo_electronico, telefono, direccion, contrasenya, tipo_usuario) 
                 VALUES (%s, %s, %s, %s, %s, %s, 'cliente')"""
        cursor.execute(sql, (nombre, apellidos, email, telefono, direccion, password_hash))
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

def obtener_usuario_por_email(email):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        print(f"🔍 Buscando email: {email}")  # DEBUG
        cursor.execute("SELECT * FROM usuarios WHERE correo_electronico = %s", (email,))
        resultado = cursor.fetchone()
        print(f"✅ Resultado: {resultado}")  # DEBUG
        return resultado
    except Exception as e:
        print(f"❌ Error: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

def verificar_password(password_hash, password_plano):
    return check_password_hash(password_hash, password_plano)

def obtener_recetas():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT receta_id, nombre, descripcion, dificultad, tiempo_preparacion, porciones, precio_venta FROM recetas WHERE activa = 1")
        return cursor.fetchall()
    except Exception as e:
        print(f"Error en obtener_recetas: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

def obtener_detalle_receta(receta_id, lang='es'):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""SELECT r.*, c.nombre as categoria FROM recetas r 
                          JOIN categorias c ON r.categoria_id = c.categoria_id 
                          WHERE r.receta_id = %s""", (receta_id,))
        receta = cursor.fetchone()
        
        if receta:
            # Obtener ingredientes
            cursor.execute("""SELECT i.ingrediente_id, i.nombre, ri.cantidad, i.unidad 
                              FROM receta_ingredientes ri 
                              JOIN ingredientes i ON ri.ingrediente_id = i.ingrediente_id 
                              WHERE ri.receta_id = %s""", (receta_id,))
            receta['ingredientes'] = cursor.fetchall()
            
            # Obtener pasos
            cursor.execute("SELECT paso_id, numero_paso, descripcion FROM pasos_receta WHERE receta_id = %s ORDER BY numero_paso", (receta_id,))
            receta['pasos'] = cursor.fetchall()
        
        return receta
    except Exception as e:
        print(f"Error en obtener_detalle_receta: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
            
def obtener_receta_por_id(receta_id):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT receta_id, nombre, precio_venta FROM recetas WHERE receta_id = %s AND activa = 1", (receta_id,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

def crear_pedido(usuario_id, direccion_envio, items_carrito):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        subtotal = sum(item['cantidad'] * item['precio'] for item in items_carrito)
        total = subtotal + 3.99
        cursor.execute("""INSERT INTO pedidos (usuario_id, fecha_entrega, estado, total, direccion_envio) 
                          VALUES (%s, DATE_ADD(CURDATE(), INTERVAL 2 DAY), 'pendiente', %s, %s)""", 
                       (usuario_id, total, direccion_envio))
        pedido_id = cursor.lastrowid
        for item in items_carrito:
            cursor.execute("INSERT INTO detalles_pedido (pedido_id, receta_id, cantidad, precio_unitario) VALUES (%s, %s, %s, %s)", 
                          (pedido_id, item['receta_id'], item['cantidad'], item['precio']))
        conn.commit()
        return pedido_id
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

def obtener_pedidos_usuario(usuario_id):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM pedidos WHERE usuario_id = %s ORDER BY fecha_pedido DESC", (usuario_id,))
        return cursor.fetchall()
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
            
def obtener_estadisticas_admin():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT COUNT(*) as total FROM usuarios")
        usuarios = cursor.fetchone()
        total_usuarios = usuarios['total'] if usuarios else 0
        
        cursor.execute("SELECT COUNT(*) as total FROM recetas")
        recetas = cursor.fetchone()
        total_recetas = recetas['total'] if recetas else 0
        
        cursor.execute("SELECT COUNT(*) as total FROM pedidos")
        pedidos = cursor.fetchone()
        total_pedidos = pedidos['total'] if pedidos else 0
        
        cursor.execute("SELECT COUNT(*) as total FROM pedidos WHERE estado = 'pendiente'")
        pendientes = cursor.fetchone()
        pedidos_pendientes = pendientes['total'] if pendientes else 0
        
        return {
            'total_usuarios': total_usuarios,
            'total_recetas': total_recetas,
            'total_pedidos': total_pedidos,
            'pedidos_pendientes': pedidos_pendientes
        }
    except Exception as e:
        print(f"Error en obtener_estadisticas_admin: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
            
def obtener_categorias():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM categorias ORDER BY nombre")
        return cursor.fetchall()
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

def guardar_receta(receta_id, nombre, descripcion, categoria_id, dificultad, tiempo, porciones, precio, activa, ingredientes=None, pasos=None):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        if receta_id:
            # Actualizar receta
            sql = """UPDATE recetas SET nombre=%s, descripcion=%s, categoria_id=%s, dificultad=%s, 
                     tiempo_preparacion=%s, porciones=%s, precio_venta=%s, activa=%s WHERE receta_id=%s"""
            cursor.execute(sql, (nombre, descripcion, categoria_id, dificultad, tiempo, porciones, precio, activa, receta_id))
        else:
            # Insertar nueva receta
            sql = """INSERT INTO recetas (nombre, descripcion, categoria_id, dificultad, tiempo_preparacion, porciones, precio_venta, activa) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (nombre, descripcion, categoria_id, dificultad, tiempo, porciones, precio, activa))
            receta_id = cursor.lastrowid
        
        # Guardar ingredientes
        if ingredientes:
            # Eliminar ingredientes antiguos
            cursor.execute("DELETE FROM receta_ingredientes WHERE receta_id = %s", (receta_id,))
            
            # Insertar nuevos ingredientes
            for ing in ingredientes:
                # Buscar o crear ingrediente
                cursor.execute("SELECT ingrediente_id FROM ingredientes WHERE nombre = %s", (ing['nombre'],))
                ing_existente = cursor.fetchone()
                if ing_existente:
                    ing_id = ing_existente[0]
                else:
                    cursor.execute("INSERT INTO ingredientes (nombre, unidad) VALUES (%s, %s)", (ing['nombre'], ing['unidad']))
                    ing_id = cursor.lastrowid
                
                cursor.execute("INSERT INTO receta_ingredientes (receta_id, ingrediente_id, cantidad) VALUES (%s, %s, %s)",
                              (receta_id, ing_id, ing['cantidad']))
        
        # Guardar pasos
        if pasos:
            # Eliminar pasos antiguos
            cursor.execute("DELETE FROM pasos_receta WHERE receta_id = %s", (receta_id,))
            
            # Insertar nuevos pasos
            for i, paso in enumerate(pasos, 1):
                cursor.execute("INSERT INTO pasos_receta (receta_id, numero_paso, descripcion) VALUES (%s, %s, %s)",
                              (receta_id, i, paso['descripcion']))
        
        conn.commit()
        return receta_id
    except Exception as e:
        print(f"Error en guardar_receta: {e}")
        conn.rollback()
        return None
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

def eliminar_receta(receta_id):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE recetas SET activa = 0 WHERE receta_id = %s", (receta_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

# ======================================================
# CONFIGURACIÓN LOGIN
# ======================================================

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id, nombre, email, tipo_usuario):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.tipo_usuario = tipo_usuario

@login_manager.user_loader
def load_user(user_id):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE usuario_id = %s", (user_id,))
        user_data = cursor.fetchone()
        if user_data:
            return User(user_data['usuario_id'], user_data['nombre'], user_data['correo_electronico'], user_data['tipo_usuario'])
        return None
    except Exception as e:
        print(f"Error en load_user: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

# ======================================================
# RUTAS PÚBLICAS (con traducciones manuales)
# ======================================================

@app.route('/')
def home():
    lang = session.get('language', 'es')
    t = load_translations(lang)
    return render_template('index.html', t=t, current_lang=lang)

@app.route('/como-funciona')
def como_funciona():
    lang = session.get('language', 'es')
    t = load_translations(lang)
    return render_template('como_funciona.html', t=t, current_lang=lang)

@app.route('/contacto')
def contacto():
    lang = session.get('language', 'es')
    t = load_translations(lang)
    return render_template('contacto.html', t=t, current_lang=lang)

# ======================================================
# RUTAS AUTENTICACIÓN
# ======================================================

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    lang = session.get('language', 'es')
    t = load_translations(lang)
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        email = request.form['email']
        telefono = request.form.get('telefono', '')
        direccion = request.form.get('direccion', '')
        password = request.form['password']
        confirm = request.form['confirm_password']
        
        if password != confirm:
            flash('Las contraseñas no coinciden', 'error')
            return render_template('registro.html', t=t, current_lang=lang)
        if len(password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres', 'error')
            return render_template('registro.html', t=t, current_lang=lang)
        if obtener_usuario_por_email(email):
            flash('Ya existe un usuario con ese email', 'error')
            return render_template('registro.html', t=t, current_lang=lang)
        if registrar_usuario(nombre, apellidos, email, telefono, direccion, password):
            flash('Registro exitoso. Inicia sesión.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Error en el registro', 'error')
    
    return render_template('registro.html', t=t, current_lang=lang)

@app.route('/login', methods=['GET', 'POST'])
def login():
    lang = session.get('language', 'es')
    t = load_translations(lang)
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        print(f"📧 Email recibido: {email}")  # DEBUG
        usuario = obtener_usuario_por_email(email)
        print(f"👤 Usuario encontrado: {usuario}")  # DEBUG
        
        if usuario:
            user = User(usuario['usuario_id'], usuario['nombre'], usuario['correo_electronico'], usuario['tipo_usuario'])
            login_user(user)
            flash(f'Bienvenido {usuario["nombre"]}', 'success')
            return redirect(url_for('admin_dashboard') if usuario['tipo_usuario'] == 'admin' else url_for('perfil'))
        else:
            flash('Email no encontrado. Regístrate primero.', 'error')
    
    return render_template('login.html', t=t, current_lang=lang)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('carrito', None)
    flash('Sesión cerrada', 'success')
    return redirect(url_for('home'))

# ======================================================
# RUTAS RECETAS
# ======================================================

@app.route('/recetas')
def recetas():
    lang = session.get('language', 'es')
    t = load_translations(lang)
    recetas = obtener_recetas()
    return render_template('recetas.html', recetas=recetas, t=t, current_lang=lang)

@app.route('/receta/<int:receta_id>')
def detalle_receta(receta_id):
    lang = session.get('language', 'es')
    t = load_translations(lang)
    receta = obtener_detalle_receta(receta_id, lang)
    if not receta:
        return "Receta no encontrada", 404
    return render_template('detalle_receta.html', receta=receta, t=t, current_lang=lang)

# ======================================================
# RUTAS CARRITO
# ======================================================

@app.route('/add-to-cart/<int:receta_id>')
@login_required
def add_to_cart(receta_id):
    if 'carrito' not in session:
        session['carrito'] = []
    receta = obtener_receta_por_id(receta_id)
    if not receta:
        flash('Receta no encontrada', 'error')
        return redirect(url_for('recetas'))
    carrito = session['carrito']
    for item in carrito:
        if item['receta_id'] == receta_id:
            item['cantidad'] += 1
            break
    else:
        carrito.append({'receta_id': receta_id, 'nombre': receta['nombre'], 'cantidad': 1, 'precio': float(receta['precio_venta'])})
    session['carrito'] = carrito
    flash(f'{receta["nombre"]} añadida al carrito', 'success')
    return redirect(request.referrer or url_for('recetas'))

@app.route('/carrito')
@login_required
def ver_carrito():
    lang = session.get('language', 'es')
    t = load_translations(lang)
    carrito = session.get('carrito', [])
    subtotal = sum(item['cantidad'] * item['precio'] for item in carrito)
    return render_template('carrito.html', carrito=carrito, subtotal=subtotal, total=subtotal + 3.99, t=t, current_lang=lang)

@app.route('/update-cart/<int:receta_id>/<int:cantidad>')
@login_required
def update_cart(receta_id, cantidad):
    if 'carrito' in session:
        carrito = session['carrito']
        for item in carrito:
            if item['receta_id'] == receta_id:
                if cantidad <= 0:
                    carrito.remove(item)
                else:
                    item['cantidad'] = cantidad
                break
        session['carrito'] = carrito
    return redirect(url_for('ver_carrito'))

@app.route('/remove-from-cart/<int:receta_id>')
@login_required
def remove_from_cart(receta_id):
    if 'carrito' in session:
        session['carrito'] = [item for item in session['carrito'] if item['receta_id'] != receta_id]
    flash('Receta eliminada del carrito', 'success')
    return redirect(url_for('ver_carrito'))

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    lang = session.get('language', 'es')
    t = load_translations(lang)
    carrito = session.get('carrito', [])
    
    if not carrito:
        flash(t['carrito_vacio'] if 'carrito_vacio' in t else 'El carrito está vacío', 'error')
        return redirect(url_for('recetas'))
    
    subtotal = sum(item['cantidad'] * item['precio'] for item in carrito)
    total = subtotal + 3.99
    
    if request.method == 'POST':
        direccion = request.form.get('direccion', '').strip()
        if not direccion:
            flash(t['flash_direccion_requerida'] if 'flash_direccion_requerida' in t else 'Por favor, proporciona una dirección de entrega', 'error')
            return render_template('checkout.html', carrito=carrito, subtotal=subtotal, total=total, t=t, current_lang=lang)
        
        pedido_id = crear_pedido(current_user.id, direccion, carrito)
        if pedido_id:
            session.pop('carrito', None)
            flash(f'¡Pedido #{pedido_id} realizado con éxito!', 'success')
            return redirect(url_for('perfil'))
        else:
            flash(t['flash_pedido_error'] if 'flash_pedido_error' in t else 'Error al procesar el pedido', 'error')
    
    return render_template('checkout.html', carrito=carrito, subtotal=subtotal, total=total, t=t, current_lang=lang)

# ======================================================
# RUTAS PERFIL
# ======================================================

@app.route('/perfil')
@login_required
def perfil():
    lang = session.get('language', 'es')
    t = load_translations(lang)
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE usuario_id = %s", (current_user.id,))
        usuario = cursor.fetchone()
        pedidos = obtener_pedidos_usuario(current_user.id)
        return render_template('perfil.html', usuario=usuario, pedidos=pedidos, t=t, current_lang=lang)
    except Exception as e:
        return f"Error: {e}"
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# ======================================================
# RUTAS ADMIN
# ======================================================

@app.route('/admin')
@login_required
def admin_dashboard():
    if current_user.tipo_usuario != 'admin':
        flash('No tienes permisos', 'error')
        return redirect(url_for('home'))
    
    lang = session.get('language', 'es')
    t = load_translations(lang)
    
    stats = obtener_estadisticas_admin()
    
    # Si stats es None, usar valores por defecto
    if stats is None:
        stats = {
            'total_usuarios': 0,
            'total_recetas': 0,
            'total_pedidos': 0,
            'pedidos_pendientes': 0
        }
    
    return render_template('admin/dashboard.html', t=t, current_lang=lang, **stats)

@app.route('/admin/recetas')
@login_required
def admin_recetas():
    if current_user.tipo_usuario != 'admin':
        flash('No tienes permisos', 'error')
        return redirect(url_for('home'))
    lang = session.get('language', 'es')
    t = load_translations(lang)
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""SELECT r.*, c.nombre as categoria FROM recetas r 
                          JOIN categorias c ON r.categoria_id = c.categoria_id 
                          ORDER BY r.receta_id DESC""")
        recetas = cursor.fetchall()
        return render_template('admin/recetas.html', recetas=recetas, t=t, current_lang=lang)
    except Exception as e:
        return f"Error: {e}"
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/admin/usuarios')
@login_required
def admin_usuarios():
    if current_user.tipo_usuario != 'admin':
        flash('No tienes permisos', 'error')
        return redirect(url_for('home'))
    lang = session.get('language', 'es')
    t = load_translations(lang)
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT usuario_id, nombre, apellidos, correo_electronico, telefono, pais, tipo_usuario, fecha_registro FROM usuarios ORDER BY fecha_registro DESC")
        usuarios = cursor.fetchall()
        return render_template('admin/usuarios.html', usuarios=usuarios, t=t, current_lang=lang)
    except Exception as e:
        return f"Error: {e}"
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/admin/pedidos')
@login_required
def admin_pedidos():
    if current_user.tipo_usuario != 'admin':
        flash('No tienes permisos', 'error')
        return redirect(url_for('home'))
    lang = session.get('language', 'es')
    t = load_translations(lang)
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT p.*, u.nombre, u.apellidos FROM pedidos p JOIN usuarios u ON p.usuario_id = u.usuario_id ORDER BY p.fecha_pedido DESC")
        pedidos = cursor.fetchall()
        return render_template('admin/pedidos.html', pedidos=pedidos, t=t, current_lang=lang)
    except Exception as e:
        return f"Error: {e}"
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/admin/recetas/nueva', methods=['GET', 'POST'])
@login_required
def admin_receta_nueva():
    if current_user.tipo_usuario != 'admin':
        flash('No tienes permisos', 'error')
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        categoria_id = request.form['categoria_id']
        dificultad = request.form['dificultad']
        tiempo = request.form['tiempo_preparacion']
        porciones = request.form['porciones']
        precio = request.form['precio_venta']
        activa = 1 if request.form.get('activa') else 0
        
        # Procesar ingredientes
        ingredientes = []
        nombres_ing = request.form.getlist('ingrediente_nombre[]')
        cantidades = request.form.getlist('ingrediente_cantidad[]')
        unidades = request.form.getlist('ingrediente_unidad[]')
        
        for i in range(len(nombres_ing)):
            if nombres_ing[i] and cantidades[i]:
                ingredientes.append({
                    'nombre': nombres_ing[i],
                    'cantidad': float(cantidades[i]),
                    'unidad': unidades[i] if i < len(unidades) else 'g'
                })
        
        # Procesar pasos
        pasos = []
        descripciones = request.form.getlist('paso_descripcion[]')
        for i, desc in enumerate(descripciones):
            if desc.strip():
                pasos.append({'descripcion': desc.strip()})
        
        receta_id = guardar_receta(None, nombre, descripcion, categoria_id, dificultad, tiempo, porciones, precio, activa, ingredientes, pasos)
        
        if receta_id:
            flash('Receta creada correctamente', 'success')
        else:
            flash('Error al crear la receta', 'error')
        return redirect(url_for('admin_recetas'))
    
    # GET: mostrar formulario
    lang = session.get('language', 'es')
    t = load_translations(lang)
    categorias = obtener_categorias()
    return render_template('admin/receta_form.html', receta=None, categorias=categorias, t=t, current_lang=lang)


@app.route('/admin/recetas/editar/<int:receta_id>', methods=['GET', 'POST'])
@login_required
def admin_receta_editar(receta_id):
    if current_user.tipo_usuario != 'admin':
        flash('No tienes permisos', 'error')
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        categoria_id = request.form['categoria_id']
        dificultad = request.form['dificultad']
        tiempo = request.form['tiempo_preparacion']
        porciones = request.form['porciones']
        precio = request.form['precio_venta']
        activa = 1 if request.form.get('activa') else 0
        
        # Procesar ingredientes
        ingredientes = []
        nombres_ing = request.form.getlist('ingrediente_nombre[]')
        cantidades = request.form.getlist('ingrediente_cantidad[]')
        unidades = request.form.getlist('ingrediente_unidad[]')
        
        for i in range(len(nombres_ing)):
            if nombres_ing[i] and cantidades[i]:
                ingredientes.append({
                    'nombre': nombres_ing[i],
                    'cantidad': float(cantidades[i]),
                    'unidad': unidades[i] if i < len(unidades) else 'g'
                })
        
        # Procesar pasos
        pasos = []
        descripciones = request.form.getlist('paso_descripcion[]')
        for i, desc in enumerate(descripciones):
            if desc.strip():
                pasos.append({'descripcion': desc.strip()})
        
        resultado = guardar_receta(receta_id, nombre, descripcion, categoria_id, dificultad, tiempo, porciones, precio, activa, ingredientes, pasos)
        
        if resultado:
            flash('Receta actualizada correctamente', 'success')
        else:
            flash('Error al actualizar la receta', 'error')
        return redirect(url_for('admin_recetas'))
    
    # GET: mostrar formulario con datos
    receta = obtener_detalle_receta(receta_id)
    if not receta:
        flash('Receta no encontrada', 'error')
        return redirect(url_for('admin_recetas'))
    
    lang = session.get('language', 'es')
    t = load_translations(lang)
    categorias = obtener_categorias()
    return render_template('admin/receta_form.html', receta=receta, categorias=categorias, t=t, current_lang=lang)

# ======================================================
# RUTA PRUEBA
# ======================================================

@app.route('/test-db')
def test_db():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM recetas")
        count = cursor.fetchone()[0]
        return f"✅ Conexión OK. {count} recetas en BD."
    except Exception as e:
        return f"❌ Error: {e}"
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# ======================================================
# ERRORES
# ======================================================

@app.errorhandler(404)
def page_not_found(e):
    lang = session.get('language', 'es')
    t = load_translations(lang)
    return render_template('404.html', t=t, current_lang=lang), 404

# ======================================================
# INICIO
# ======================================================

if __name__ == '__main__':
    app.run(debug=True)