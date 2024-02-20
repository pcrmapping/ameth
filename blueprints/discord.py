from flask import Blueprint

bp = Blueprint('discord', __name__, url_prefix='/_discord')

@bp.route('/hook')
def interaction_hook():
    return