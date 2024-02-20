from flask import Blueprint

bp = Blueprint('admin', __name__, url_prefix='/shh')

@bp.route('/')
def dashboard():
    return