from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from DAO.usuarioDAO import UsuarioDAO

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        usuario = UsuarioDAO.buscar_por_username(username)
        if usuario and usuario.password == password:
            login_user(usuario)
            return redirect(url_for('inicio.index'))
        flash('Usuario o contraseña incorrectos.', 'danger')
    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))