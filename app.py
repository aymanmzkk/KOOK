from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
import os

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
# FUNCIONES BD
# ======================================================

def get_connection():
    return mysql.connector.connect(**db_config)

# Registrar usuario
def registrar_usuario(nombre, apellidos, email, telefono, direccion, password):
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
        if conn.is_connected():
            cursor.close()
            conn.close()

# Buscar usuario por email
def obtener_usuario_por_email(email):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE correo_electronico = %s", (email,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Verificar contraseña
def verificar_password(password_hash, password_plano):
    return check_password_hash(password_hash, password_plano)

# Obtener recetas
def obtener_recetas():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT receta_id, nombre, descripcion, dificultad, tiempo_preparacion, porciones, precio_venta FROM recetas WHERE activa = 1")
        return cursor.fetchall()
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Obtener detalle completo de una receta
def obtener_detalle_receta(receta_id):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Obtener datos básicos de la receta
        cursor.execute("""
            SELECT r.*, c.nombre as categoria 
            FROM recetas r
            JOIN categorias c ON r.categoria_id = c.categoria_id
            WHERE r.receta_id = %s AND r.activa = 1
        """, (receta_id,))
        
        receta = cursor.fetchone()
        
        if receta:
            # Obtener ingredientes
            cursor.execute("""
                SELECT i.nombre, ri.cantidad, i.unidad
                FROM receta_ingredientes ri
                JOIN ingredientes i ON ri.ingrediente_id = i.ingrediente_id
                WHERE ri.receta_id = %s
            """, (receta_id,))
            receta['ingredientes'] = cursor.fetchall()
            print(f"Ingredientes encontrados: {len(receta['ingredientes'])}")  # Debug
            
            # Obtener pasos
            cursor.execute("""
                SELECT numero_paso, descripcion
                FROM pasos_receta
                WHERE receta_id = %s
                ORDER BY numero_paso
            """, (receta_id,))
            receta['pasos'] = cursor.fetchall()
            print(f"Pasos encontrados: {len(receta['pasos'])}")  # Debug
        
        cursor.close()
        conn.close()
        return receta
        
    except Exception as e:
        print(f"Error en obtener_detalle_receta: {e}")
        return None

# Obtener receta para carrito
def obtener_receta_por_id(receta_id):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT receta_id, nombre, precio_venta FROM recetas WHERE receta_id = %s AND activa = 1", (receta_id,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Crear pedido
def crear_pedido(usuario_id, direccion_envio, items_carrito):
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
        if conn.is_connected():
            cursor.close()
            conn.close()

# Obtener pedidos usuario
def obtener_pedidos_usuario(usuario_id):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM pedidos WHERE usuario_id = %s ORDER BY fecha_pedido DESC", (usuario_id,))
        return cursor.fetchall()
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Obtener estadísticas admin
def obtener_estadisticas_admin():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) as total FROM usuarios")
        usuarios = cursor.fetchone()['total']
        cursor.execute("SELECT COUNT(*) as total FROM recetas")
        recetas = cursor.fetchone()['total']
        cursor.execute("SELECT COUNT(*) as total FROM pedidos")
        pedidos = cursor.fetchone()['total']
        cursor.execute("SELECT COUNT(*) as total FROM pedidos WHERE estado = 'pendiente'")
        pendientes = cursor.fetchone()['total']
        return {'total_usuarios': usuarios, 'total_recetas': recetas, 'total_pedidos': pedidos, 'pedidos_pendientes': pendientes}
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Obtener categorías
def obtener_categorias():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM categorias ORDER BY nombre")
        return cursor.fetchall()
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Guardar receta
def guardar_receta(receta_id, nombre, descripcion, categoria_id, dificultad, tiempo, porciones, precio, activa):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        if receta_id:
            sql = """UPDATE recetas SET nombre=%s, descripcion=%s, categoria_id=%s, dificultad=%s, 
                     tiempo_preparacion=%s, porciones=%s, precio_venta=%s, activa=%s WHERE receta_id=%s"""
            cursor.execute(sql, (nombre, descripcion, categoria_id, dificultad, tiempo, porciones, precio, activa, receta_id))
        else:
            sql = """INSERT INTO recetas (nombre, descripcion, categoria_id, dificultad, tiempo_preparacion, porciones, precio_venta, activa) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (nombre, descripcion, categoria_id, dificultad, tiempo, porciones, precio, activa))
            receta_id = cursor.lastrowid
        conn.commit()
        return receta_id
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Eliminar receta
def eliminar_receta(receta_id):
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
        if conn.is_connected():
            cursor.close()
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
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE usuario_id = %s", (user_id,))
        user_data = cursor.fetchone()
        if user_data:
            return User(user_data['usuario_id'], user_data['nombre'], user_data['correo_electronico'], user_data['tipo_usuario'])
        return None
    except:
        return None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# ======================================================
# RUTAS PÚBLICAS
# ======================================================

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/como-funciona')
def como_funciona():
    return render_template('como_funciona.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

# ======================================================
# RUTAS AUTENTICACIÓN
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
        confirm = request.form['confirm_password']
        
        if password != confirm:
            flash('Las contraseñas no coinciden', 'error')
            return render_template('registro.html')
        
        if obtener_usuario_por_email(email):
            flash('Email ya registrado', 'error')
            return render_template('registro.html')
        
        if registrar_usuario(nombre, apellidos, email, telefono, direccion, password):
            flash('Registro exitoso. Inicia sesión.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Error en el registro', 'error')
    
    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        usuario = obtener_usuario_por_email(email)
        
        if usuario and verificar_password(usuario['contrasenya'], password):
            user = User(usuario['usuario_id'], usuario['nombre'], usuario['correo_electronico'], usuario['tipo_usuario'])
            login_user(user)
            return redirect(url_for('admin_dashboard') if usuario['tipo_usuario'] == 'admin' else url_for('perfil'))
        else:
            flash('Email o contraseña incorrectos', 'error')
    
    return render_template('login.html')

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
    return render_template('recetas.html', recetas=obtener_recetas())

@app.route('/receta/<int:receta_id>')
def detalle_receta(receta_id):
    receta = obtener_detalle_receta(receta_id)
    if not receta:
        return "Receta no encontrada", 404
    print(f"Receta cargada: {receta['nombre']}")  # Debug
    return render_template('detalle_receta.html', receta=receta)

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
    carrito = session.get('carrito', [])
    subtotal = sum(item['cantidad'] * item['precio'] for item in carrito)
    return render_template('carrito.html', carrito=carrito, subtotal=subtotal, total=subtotal + 3.99)

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
    flash('Receta eliminada', 'success')
    return redirect(url_for('ver_carrito'))

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    carrito = session.get('carrito', [])
    if not carrito:
        flash('Carrito vacío', 'error')
        return redirect(url_for('recetas'))
    
    subtotal = sum(item['cantidad'] * item['precio'] for item in carrito)
    total = subtotal + 3.99
    
    if request.method == 'POST':
        direccion = request.form.get('direccion', '').strip()
        if not direccion:
            flash('Dirección requerida', 'error')
            return render_template('checkout.html', carrito=carrito, subtotal=subtotal, total=total)
        
        pedido_id = crear_pedido(current_user.id, direccion, carrito)
        if pedido_id:
            session.pop('carrito', None)
            flash(f'Pedido #{pedido_id} realizado', 'success')
            return redirect(url_for('perfil'))
        else:
            flash('Error al procesar pedido', 'error')
    
    return render_template('checkout.html', carrito=carrito, subtotal=subtotal, total=total)

# ======================================================
# RUTAS PERFIL
# ======================================================

@app.route('/perfil')
@login_required
def perfil():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE usuario_id = %s", (current_user.id,))
        usuario = cursor.fetchone()
        pedidos = obtener_pedidos_usuario(current_user.id)
        return render_template('perfil.html', usuario=usuario, pedidos=pedidos)
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
        flash('Acceso denegado', 'error')
        return redirect(url_for('home'))
    return render_template('admin/dashboard.html', **obtener_estadisticas_admin())

@app.route('/admin/recetas')
@login_required
def admin_recetas():
    if current_user.tipo_usuario != 'admin':
        flash('Acceso denegado', 'error')
        return redirect(url_for('home'))
    
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""SELECT r.*, c.nombre as categoria FROM recetas r 
                          JOIN categorias c ON r.categoria_id = c.categoria_id 
                          ORDER BY r.receta_id DESC""")
        recetas = cursor.fetchall()
        return render_template('admin/recetas.html', recetas=recetas)
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
        flash('Acceso denegado', 'error')
        return redirect(url_for('home'))
    
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT usuario_id, nombre, apellidos, correo_electronico, telefono, pais, tipo_usuario, fecha_registro FROM usuarios ORDER BY fecha_registro DESC")
        return render_template('admin/usuarios.html', usuarios=cursor.fetchall())
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
        flash('Acceso denegado', 'error')
        return redirect(url_for('home'))
    
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT p.*, u.nombre, u.apellidos FROM pedidos p JOIN usuarios u ON p.usuario_id = u.usuario_id ORDER BY p.fecha_pedido DESC")
        return render_template('admin/pedidos.html', pedidos=cursor.fetchall())
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
        flash('Acceso denegado', 'error')
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
        
        if guardar_receta(None, nombre, descripcion, categoria_id, dificultad, tiempo, porciones, precio, activa):
            flash('Receta creada', 'success')
        else:
            flash('Error al crear receta', 'error')
        return redirect(url_for('admin_recetas'))
    
    return render_template('admin/receta_form.html', receta=None, categorias=obtener_categorias())

@app.route('/admin/recetas/editar/<int:receta_id>', methods=['GET', 'POST'])
@login_required
def admin_receta_editar(receta_id):
    if current_user.tipo_usuario != 'admin':
        flash('Acceso denegado', 'error')
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
        
        if guardar_receta(receta_id, nombre, descripcion, categoria_id, dificultad, tiempo, porciones, precio, activa):
            flash('Receta actualizada', 'success')
        else:
            flash('Error al actualizar', 'error')
        return redirect(url_for('admin_recetas'))
    
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM recetas WHERE receta_id = %s", (receta_id,))
        receta = cursor.fetchone()
        return render_template('admin/receta_form.html', receta=receta, categorias=obtener_categorias())
    except Exception as e:
        flash(f'Error: {e}', 'error')
        return redirect(url_for('admin_recetas'))
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/admin/recetas/eliminar/<int:receta_id>')
@login_required
def admin_receta_eliminar(receta_id):
    if current_user.tipo_usuario != 'admin':
        flash('Acceso denegado', 'error')
        return redirect(url_for('home'))
    
    if eliminar_receta(receta_id):
        flash('Receta eliminada', 'success')
    else:
        flash('Error al eliminar', 'error')
    return redirect(url_for('admin_recetas'))

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
    return render_template('404.html'), 404

# ======================================================
# INICIO
# ======================================================

if __name__ == '__main__':
    app.run(debug=True)