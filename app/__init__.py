from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Agregar la clave secreta para las sesiones
app.config['SECRET_KEY'] = 'clave_super_secreta_123'

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://usuario:contraseña@localhost/banco_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from app import routes
