from flask import Blueprint

bp = Blueprint('physio', __name__)

from app.physio import routes