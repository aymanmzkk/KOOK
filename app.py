from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
import os

# FORZAR LA RUTA DE TEMPLATES
template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=template_dir)

# Opcional: imprimir para verificar
print(f"✅ Templates buscando en: {template_dir}")
print(f"✅ ¿Existe? {os.path.exists(template_dir)}")

app.secret_key = 'clave-secreta-muy-dificil-koook-2026-para-proyecto-dam'
app.permanent_session_lifetime = timedelta(days=7)

# Configuración de la base de datos
db_config = {
    'host': 'localhost',
    'user': 'usuario-kook',
    'password': 'Kook2026$',
    'database': 'KOOK',
    'port': 3306
}

# ======================================================
# FUNCIONES DE BASE DE DATOS (con mysql.connector directo)
# ======================================================

# Registrar nuevo usuario
def registrar_usuario(nombre, apellidos, email, telefono, direccion, password):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        password_hash = generate_password_hash(password)
        
        sql = """
            INSERT INTO usuarios 
            (nombre, apellidos, correo_electronico, telefono, direccion, contrasenya, tipo_usuario)
            VALUES (%s, %s, %s, %s, %s, %s, 'cliente')
        """
        valores = (nombre, apellidos, email, telefono, direccion, password_hash)
        
        cursor.execute(sql, valores)
        conn.commit()
        
        return cursor.lastrowid
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Buscar usuario por email
def obtener_usuario_por_email(email):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        sql = "SELECT * FROM usuarios WHERE correo_electronico = %s"
        cursor.execute(sql, (email,))
        usuario = cursor.fetchone()
        
        return usuario
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Verificar contraseña
def verificar_password(password_hash, password_plano):
    return check_password_hash(password_hash, password_plano)

# Obtener receta por ID para carrito
def obtener_receta_por_id(receta_id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT receta_id, nombre, precio_venta 
            FROM recetas 
            WHERE receta_id = %s AND activa = 1
        """, (receta_id,))
        
        receta = cursor.fetchone()
        return receta
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Crear pedido
def crear_pedido(usuario_id, direccion_envio, items_carrito):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        subtotal = sum(item['cantidad'] * item['precio'] for item in items_carrito)
        gastos_envio = 3.99
        total = subtotal + gastos_envio
        
        sql_pedido = """
            INSERT INTO pedidos (usuario_id, fecha_entrega, estado, total, direccion_envio)
            VALUES (%s, DATE_ADD(CURDATE(), INTERVAL 2 DAY), 'pendiente', %s, %s)
        """
        cursor.execute(sql_pedido, (usuario_id, total, direccion_envio))
        pedido_id = cursor.lastrowid
        
        sql_detalle = """
            INSERT INTO detalles_pedido (pedido_id, receta_id, cantidad, precio_unitario)
            VALUES (%s, %s, %s, %s)
        """
        for item in items_carrito:
            cursor.execute(sql_detalle, (pedido_id, item['receta_id'], item['cantidad'], item['precio']))
        
        conn.commit()
        return pedido_id
        
    except mysql.connector.Error as err:
        print(f"Error al crear pedido: {err}")
        if conn:
            conn.rollback()
        return None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Obtener pedidos de un usuario
def obtener_pedidos_usuario(usuario_id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT p.*, 
                   (SELECT COUNT(*) FROM detalles_pedido WHERE pedido_id = p.pedido_id) as num_recetas
            FROM pedidos p
            WHERE p.usuario_id = %s
            ORDER BY p.fecha_pedido DESC
        """, (usuario_id,))
        
        pedidos = cursor.fetchall()
        return pedidos
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Obtener todas las recetas activas
def obtener_recetas():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT receta_id, nombre, descripcion, dificultad, 
                   tiempo_preparacion, porciones, precio_venta
            FROM recetas 
            WHERE activa = 1
        """)
        
        recetas = cursor.fetchall()
        cursor.close()
        conn.close()
        return recetas
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []

# Obtener detalle completo de una receta
def obtener_detalle_receta(receta_id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT r.*, c.nombre as categoria 
            FROM recetas r
            JOIN categorias c ON r.categoria_id = c.categoria_id
            WHERE r.receta_id = %s AND r.activa = 1
        """, (receta_id,))
        
        receta = cursor.fetchone()
        
        if receta:
            cursor.execute("""
                SELECT i.nombre, ri.cantidad, i.unidad
                FROM receta_ingredientes ri
                JOIN ingredientes i ON ri.ingrediente_id = i.ingrediente_id
                WHERE ri.receta_id = %s
            """, (receta_id,))
            receta['ingredientes'] = cursor.fetchall()
            
            cursor.execute("""
                SELECT numero_paso, descripcion
                FROM pasos_receta
                WHERE receta_id = %s
                ORDER BY numero_paso
            """, (receta_id,))
            receta['pasos'] = cursor.fetchall()
        
        return receta
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Obtener estadísticas para admin
def obtener_estadisticas_admin():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT COUNT(*) as total FROM usuarios")
        total_usuarios = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as total FROM recetas")
        total_recetas = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as total FROM pedidos")
        total_pedidos = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as total FROM pedidos WHERE estado = 'pendiente'")
        pedidos_pendientes = cursor.fetchone()['total']
        
        cursor.close()
        conn.close()
        
        return {
            'total_usuarios': total_usuarios,
            'total_recetas': total_recetas,
            'total_pedidos': total_pedidos,
            'pedidos_pendientes': pedidos_pendientes
        }
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# ======================================================
# CONFIGURACIÓN FLASK-LOGIN
# ======================================================

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor, inicia sesión para acceder a esta página.'
login_manager.login_message_category = 'error'

class User(UserMixin):
    def __init__(self, id, nombre, email, tipo_usuario):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.tipo_usuario = tipo_usuario

@login_manager.user_loader
def load_user(user_id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE usuario_id = %s", (user_id,))
        user_data = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if user_data:
            return User(
                id=user_data['usuario_id'],
                nombre=user_data['nombre'],
                email=user_data['correo_electronico'],
                tipo_usuario=user_data['tipo_usuario']
            )
        return None
    except:
        return None

# ======================================================
# RUTAS PÚBLICAS
# ======================================================

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/como-funciona')
def como_funciona():
    return render_template('como_funciona.html')

@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    if request.method == 'POST':
        flash('Mensaje enviado correctamente. Te responderemos pronto.', 'success')
        return redirect(url_for('contacto'))
    return render_template('contacto.html')

# ======================================================
# RUTAS DE AUTENTICACIÓN
# ======================================================

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        email = request.form['email']
        telefono = request.form.get('telefono', '')
        direccion = request.form.get('direccion', '')
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash('Las contraseñas no coinciden', 'error')
            return render_template('registro.html')
        
        if len(password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres', 'error')
            return render_template('registro.html')
        
        usuario_existente = obtener_usuario_por_email(email)
        if usuario_existente:
            flash('Ya existe un usuario con ese email', 'error')
            return render_template('registro.html')
        
        user_id = registrar_usuario(nombre, apellidos, email, telefono, direccion, password)
        
        if user_id:
            flash('Registro exitoso. Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Error en el registro. Inténtalo de nuevo.', 'error')
            return render_template('registro.html')
    
    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        usuario = obtener_usuario_por_email(email)
        
        if usuario and verificar_password(usuario['contrasenya'], password):
            user = User(
                id=usuario['usuario_id'],
                nombre=usuario['nombre'],
                email=usuario['correo_electronico'],
                tipo_usuario=usuario['tipo_usuario']
            )
            login_user(user, remember=True)
            
            if usuario['tipo_usuario'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('perfil'))
        else:
            flash('Email o contraseña incorrectos', 'error')
            return render_template('login.html')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('carrito', None)
    flash('Sesión cerrada correctamente', 'success')
    return redirect(url_for('home'))

# ======================================================
# RUTAS DE RECETAS
# ======================================================

@app.route('/recetas')
def recetas():
    recetas = obtener_recetas()
    return render_template('recetas.html', recetas=recetas)

@app.route('/receta/<int:receta_id>')
def detalle_receta(receta_id):
    receta = obtener_detalle_receta(receta_id)
    if not receta:
        return "Receta no encontrada", 404
    return render_template('detalle_receta.html', receta=receta)

# ======================================================
# RUTAS DEL CARRITO
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
    encontrado = False
    
    for item in carrito:
        if item['receta_id'] == receta_id:
            item['cantidad'] += 1
            encontrado = True
            break
    
    if not encontrado:
        carrito.append({
            'receta_id': receta_id,
            'nombre': receta['nombre'],
            'cantidad': 1,
            'precio': float(receta['precio_venta']) if receta['precio_venta'] else 14.99
        })
    
    session['carrito'] = carrito
    flash(f'¡{receta["nombre"]} añadida al carrito!', 'success')
    
    return redirect(request.referrer or url_for('recetas'))

@app.route('/carrito')
@login_required
def ver_carrito():
    carrito = session.get('carrito', [])
    subtotal = sum(item['cantidad'] * item['precio'] for item in carrito)
    gastos_envio = 3.99
    total = subtotal + gastos_envio
    return render_template('carrito.html', carrito=carrito, subtotal=subtotal, total=total)

@app.route('/update-cart/<int:receta_id>/<int:cantidad>')
@login_required
def update_cart(receta_id, cantidad):
    if 'carrito' in session:
        carrito = session['carrito']
        for item in carrito:
            if item['receta_id'] == receta_id:
                if cantidad <= 0:
                    carrito.remove(item)
                    flash('Receta eliminada del carrito', 'success')
                else:
                    item['cantidad'] = cantidad
                break
        session['carrito'] = carrito
    return redirect(url_for('ver_carrito'))

@app.route('/remove-from-cart/<int:receta_id>')
@login_required
def remove_from_cart(receta_id):
    if 'carrito' in session:
        carrito = session['carrito']
        session['carrito'] = [item for item in carrito if item['receta_id'] != receta_id]
        flash('Receta eliminada del carrito', 'success')
    return redirect(url_for('ver_carrito'))

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    carrito = session.get('carrito', [])
    
    if not carrito:
        flash('El carrito está vacío', 'error')
        return redirect(url_for('recetas'))
    
    subtotal = sum(item['cantidad'] * item['precio'] for item in carrito)
    gastos_envio = 3.99
    total = subtotal + gastos_envio
    
    if request.method == 'POST':
        direccion = request.form.get('direccion', '').strip()
        
        if not direccion:
            try:
                conn = mysql.connector.connect(**db_config)
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT direccion FROM usuarios WHERE usuario_id = %s", (current_user.id,))
                usuario = cursor.fetchone()
                direccion = usuario.get('direccion', '') if usuario else ''
                cursor.close()
                conn.close()
            except:
                pass
        
        if not direccion:
            flash('Por favor, proporciona una dirección de entrega', 'error')
            return render_template('checkout.html', carrito=carrito, subtotal=subtotal, total=total)
        
        pedido_id = crear_pedido(current_user.id, direccion, carrito)
        
        if pedido_id:
            session.pop('carrito', None)
            flash(f'¡Pedido #{pedido_id} realizado con éxito!', 'success')
            return redirect(url_for('perfil'))
        else:
            flash('Error al procesar el pedido. Inténtalo de nuevo.', 'error')
            return render_template('checkout.html', carrito=carrito, subtotal=subtotal, total=total)
    
    return render_template('checkout.html', carrito=carrito, subtotal=subtotal, total=total)

# ======================================================
# RUTAS DE PERFIL
# ======================================================

@app.route('/perfil')
@login_required
def perfil():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT usuario_id, nombre, apellidos, correo_electronico, 
                   telefono, direccion, pais, fecha_registro
            FROM usuarios WHERE usuario_id = %s
        """, (current_user.id,))
        
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()
        
        pedidos = obtener_pedidos_usuario(current_user.id)
        
        return render_template('perfil.html', usuario=usuario, pedidos=pedidos)
    except Exception as e:
        return f"Error: {e}"

# ======================================================
# RUTAS DE ADMINISTRACIÓN
# ======================================================

@app.route('/admin')
@login_required
def admin_dashboard():
    if current_user.tipo_usuario != 'admin':
        flash('No tienes permisos para acceder', 'error')
        return redirect(url_for('home'))
    
    stats = obtener_estadisticas_admin()
    return render_template('admin/dashboard.html', **stats)

@app.route('/admin/recetas')
@login_required
def admin_recetas():
    if current_user.tipo_usuario != 'admin':
        flash('No tienes permisos para acceder', 'error')
        return redirect(url_for('home'))
    
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT r.*, c.nombre as categoria 
            FROM recetas r
            JOIN categorias c ON r.categoria_id = c.categoria_id
            ORDER BY r.receta_id DESC
        """)
        
        recetas = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return render_template('admin/recetas.html', recetas=recetas)
    except Exception as e:
        return f"Error al cargar las recetas: {e}"

@app.route('/admin/usuarios')
@login_required
def admin_usuarios():
    if current_user.tipo_usuario != 'admin':
        flash('No tienes permisos para acceder', 'error')
        return redirect(url_for('home'))
    
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT usuario_id, nombre, apellidos, correo_electronico, 
                   telefono, pais, tipo_usuario, fecha_registro
            FROM usuarios
            ORDER BY fecha_registro DESC
        """)
        
        usuarios = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return render_template('admin/usuarios.html', usuarios=usuarios)
    except Exception as e:
        return f"Error al cargar los usuarios: {e}"

@app.route('/admin/pedidos')
@login_required
def admin_pedidos():
    if current_user.tipo_usuario != 'admin':
        flash('No tienes permisos para acceder', 'error')
        return redirect(url_for('home'))
    
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT p.*, u.nombre, u.apellidos 
            FROM pedidos p
            JOIN usuarios u ON p.usuario_id = u.usuario_id
            ORDER BY p.fecha_pedido DESC
        """)
        
        pedidos = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return render_template('admin/pedidos.html', pedidos=pedidos)
    except Exception as e:
        return f"Error al cargar los pedidos: {e}"

# ======================================================
# RUTA DE PRUEBA
# ======================================================

@app.route('/test-db')
def test_db():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM recetas")
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return f"✅ Conexión exitosa. Hay {count} recetas en la base de datos."
    except Exception as e:
        return f"❌ Error de conexión: {e}"

# ======================================================
# MANEJADOR DE ERRORES
# ======================================================

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    flash('Error interno del servidor. Inténtalo más tarde.', 'error')
    return redirect(url_for('home'))

# ======================================================
# FUNCIONES ADICIONALES PARA ADMIN (CRUD COMPLETO)
# ======================================================

def obtener_categorias():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM categorias ORDER BY nombre")
        categorias = cursor.fetchall()
        cursor.close()
        conn.close()
        return categorias
    except Exception as e:
        print(f"Error: {e}")
        return []

def guardar_receta(nombre, descripcion, categoria_id, dificultad, tiempo, porciones, precio, activa, receta_id=None):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        if receta_id:  # Actualizar
            sql = """
                UPDATE recetas 
                SET nombre=%s, descripcion=%s, categoria_id=%s, dificultad=%s, 
                    tiempo_preparacion=%s, porciones=%s, precio_venta=%s, activa=%s
                WHERE receta_id=%s
            """
            cursor.execute(sql, (nombre, descripcion, categoria_id, dificultad, tiempo, porciones, precio, activa, receta_id))
        else:  # Insertar nueva
            sql = """
                INSERT INTO recetas (nombre, descripcion, categoria_id, dificultad, tiempo_preparacion, porciones, precio_venta, activa)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (nombre, descripcion, categoria_id, dificultad, tiempo, porciones, precio, activa))
            receta_id = cursor.lastrowid
        
        conn.commit()
        cursor.close()
        conn.close()
        return receta_id
    except Exception as e:
        print(f"Error: {e}")
        return None

def eliminar_receta(receta_id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Opción: Desactivar en lugar de eliminar (recomendado)
        cursor.execute("UPDATE recetas SET activa = 0 WHERE receta_id = %s", (receta_id,))
        
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

# ======================================================
# RUTAS POST PARA ADMIN
# ======================================================

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
        
        receta_id = guardar_receta(None, nombre, descripcion, categoria_id, dificultad, tiempo, porciones, precio, activa)
        
        if receta_id:
            flash('Receta creada correctamente', 'success')
        else:
            flash('Error al crear la receta', 'error')
        
        return redirect(url_for('admin_recetas'))
    
    # GET: mostrar formulario
    categorias = obtener_categorias()
    return render_template('admin/receta_form.html', receta=None, categorias=categorias)

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
        
        resultado = guardar_receta(receta_id, nombre, descripcion, categoria_id, dificultad, tiempo, porciones, precio, activa)
        
        if resultado:
            flash('Receta actualizada correctamente', 'success')
        else:
            flash('Error al actualizar la receta', 'error')
        
        return redirect(url_for('admin_recetas'))
    
    # GET: mostrar formulario con datos
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM recetas WHERE receta_id = %s", (receta_id,))
        receta = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not receta:
            flash('Receta no encontrada', 'error')
            return redirect(url_for('admin_recetas'))
        
        categorias = obtener_categorias()
        return render_template('admin/receta_form.html', receta=receta, categorias=categorias)
    except Exception as e:
        flash(f'Error: {e}', 'error')
        return redirect(url_for('admin_recetas'))

@app.route('/admin/recetas/eliminar/<int:receta_id>')
@login_required
def admin_receta_eliminar(receta_id):
    if current_user.tipo_usuario != 'admin':
        flash('No tienes permisos', 'error')
        return redirect(url_for('home'))
    
    if eliminar_receta(receta_id):
        flash('Receta eliminada/desactivada correctamente', 'success')
    else:
        flash('Error al eliminar la receta', 'error')
    
    return redirect(url_for('admin_recetas'))

# ======================================================
# INICIO DE LA APLICACIÓN
# ======================================================

if __name__ == '__main__':
    app.run(debug=True)