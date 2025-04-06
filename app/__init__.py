from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Agregar la clave secreta para las sesiones
app.config['SECRET_KEY'] = 'clave_super_secreta_123'

# Configuración de la base de datos en db4free.net
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://eduardocv:Balma2025!@db4free.net:3306/bancoappcv'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from app import routes
