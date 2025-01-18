from flask import Flask

app = Flask(__name__)
app.secret_key = 'Balma1989'

from app import routes  # Importar las rutas después de crear 'app'
