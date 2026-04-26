from flask import Flask
from flask_login import LoginManager
from blueprints.auth import auth_bp
from blueprints.inicio import inicio_bp
from blueprints.pulseras import pulseras_bp
from blueprints.reparto import reparto_bp
from blueprints.cobros import cobro_bp
from blueprints.porton import porton_bp
from blueprints.admin import admin_bp
from blueprints.reportes import reportes_bp
from conexion import Conexion
from DAO.usuarioDAO import UsuarioDAO
from entidades.Usuarios import Usuario

app = Flask(__name__)
app.secret_key = 'schoolpulse_2026_colegio_panchito'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Necesitás iniciar sesión para acceder.'
login_manager.login_message_category = 'warning'


@login_manager.user_loader
def load_user(user_id):
    conexion = None
    try:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('SELECT * FROM usuario WHERE id = %s', (user_id,))
        registro = cursor.fetchone()
        if registro:
            return Usuario(registro[0], registro[1], registro[2], registro[3])
        return None
    except:
        return None
    finally:
        if conexion is not None:
            cursor.close()
            Conexion.liberar_conexion(conexion)


app.register_blueprint(auth_bp)
app.register_blueprint(inicio_bp)
app.register_blueprint(pulseras_bp)
app.register_blueprint(reparto_bp)
app.register_blueprint(cobro_bp)
app.register_blueprint(porton_bp)
app.register_blueprint(reportes_bp)
app.register_blueprint(admin_bp)

if __name__ == '__main__':
    Conexion.obtener_pool()
    app.run(debug=True)