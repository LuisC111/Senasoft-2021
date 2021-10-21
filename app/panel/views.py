from flask import redirect, url_for, render_template
from . import panel
from flask_login import login_manager, login_user, LoginManager, login_required, logout_user, current_user
from ..models import Usuario, db
from ..auth.views import login_manager

@login_manager.user_loader
def load_user(user_id):
    try:
        return Usuario.query.get(user_id)
    except:
        return None

@panel.route('/')
@login_required
def panelInicio():
    return render_template('panelUsuario.html')

@panel.route('/calendar')
@login_required
def panelCalendar():
    return render_template('panelCalendar.html')

@panel.route('/usuarios')
@login_required
def panelUsuarios():
    return render_template('datatablesPanelUsuario.html')

@panel.route('/editarPerfil')
def panelUsuarioss():
    return render_template('editarPerfilUsuario.html')