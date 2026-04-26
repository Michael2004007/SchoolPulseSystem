from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from functools import wraps
from DAO.usuarioDAO import UsuarioDAO
from entidades.Usuarios import Usuario
from werkzeug.utils import secure_filename
import os

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def solo_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.rol != 'admin':
            flash('No tenés permisos para acceder a esta sección.', 'danger')
            return redirect(url_for('inicio.index'))
        return f(*args, **kwargs)
    return decorated


def get_logo_info():
    logo_existe = False
    logo_ext = 'png'
    upload_path = os.path.join(current_app.root_path, 'static', 'uploads')
    for ext in ['png', 'jpg', 'jpeg', 'webp']:
        if os.path.exists(os.path.join(upload_path, f'logo_colegio.{ext}')):
            logo_existe = True
            logo_ext = ext
            break
    return logo_existe, logo_ext


@admin_bp.route('/')
@login_required
@solo_admin
def index():
    usuarios = UsuarioDAO.seleccionar()
    logo_existe, logo_ext = get_logo_info()
    return render_template('admin/index.html',
                           usuarios=usuarios,
                           logo_existe=logo_existe,
                           logo_ext=logo_ext)


@admin_bp.route('/crear', methods=['GET', 'POST'])
@login_required
@solo_admin
def crear():
    if request.method == 'POST':
        nombre = request.form['nombre'].strip()
        username = request.form['username'].strip()
        password = request.form['password']
        rol = request.form['rol']
        usuario = Usuario(None, username, password, rol, nombre)
        resultado = UsuarioDAO.insertar(usuario)
        if resultado:
            flash(f'✅ Usuario {nombre} creado correctamente.', 'success')
        else:
            flash('❌ Error al crear el usuario.', 'danger')
        return redirect(url_for('admin.index'))
    return render_template('admin/crear.html')


@admin_bp.route('/eliminar/<int:usuario_id>', methods=['POST'])
@login_required
@solo_admin
def eliminar(usuario_id):
    if usuario_id == current_user.id:
        flash('❌ No podés eliminar tu propio usuario.', 'danger')
        return redirect(url_for('admin.index'))
    UsuarioDAO.eliminar(usuario_id)
    flash('✅ Usuario eliminado correctamente.', 'success')
    return redirect(url_for('admin.index'))


@admin_bp.route('/editar/<int:usuario_id>', methods=['GET', 'POST'])
@login_required
@solo_admin
def editar(usuario_id):
    usuarios = UsuarioDAO.seleccionar()
    usuario = next((u for u in usuarios if u.id == usuario_id), None)
    if not usuario:
        flash('❌ Usuario no encontrado.', 'danger')
        return redirect(url_for('admin.index'))
    if request.method == 'POST':
        usuario.nombre = request.form['nombre'].strip()
        usuario.username = request.form['username'].strip()
        usuario.rol = request.form['rol']
        if request.form['password']:
            usuario.password = request.form['password']
        UsuarioDAO.actualizar(usuario)
        flash(f'✅ Usuario {usuario.nombre} actualizado correctamente.', 'success')
        return redirect(url_for('admin.index'))
    return render_template('admin/editar.html', usuario=usuario)


@admin_bp.route('/subir-logo', methods=['POST'])
@login_required
@solo_admin
def subir_logo():
    if 'logo' not in request.files:
        flash('❌ No se seleccionó ningún archivo.', 'danger')
        return redirect(url_for('admin.index'))

    file = request.files['logo']

    if file.filename == '':
        flash('❌ No se seleccionó ningún archivo.', 'danger')
        return redirect(url_for('admin.index'))

    if file and allowed_file(file.filename):
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f'logo_colegio.{ext}'
        upload_path = os.path.join(current_app.root_path, 'static', 'uploads')
        os.makedirs(upload_path, exist_ok=True)

        for e in ALLOWED_EXTENSIONS:
            old = os.path.join(upload_path, f'logo_colegio.{e}')
            if os.path.exists(old):
                os.remove(old)

        file.save(os.path.join(upload_path, filename))
        flash('✅ Logo actualizado correctamente.', 'success')
    else:
        flash('❌ Formato no permitido. Solo PNG, JPG o WEBP.', 'danger')

    return redirect(url_for('admin.index'))