from flask import Blueprint
from flask import current_app as app
from flask import request

main_bp = Blueprint("main_bp", __name__)

@main_bp.route('/', methods=['GET'])
def hello_root():
    return f"""
    Hello, World! '{request.path}'
    <p><a href=dash>dash</a>
    <p><a href=another_route>another_route</a>
    """

@main_bp.route('/another_route/', methods=['GET'])
def hello_flask():
    return f"Hello, World! '{request.path}'"
