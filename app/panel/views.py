from flask import redirect, url_for, render_template
from . import panel

@panel.route('/')
def panelInicio():
    return render_template('panelCalendar.html')

@panel.route('/usuarios')
def panelUsuarioss():
    return "hello cara de colita asdasdsa"