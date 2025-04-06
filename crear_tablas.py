from app import db
from flask import Flask
from app import app

with app.app_context():
    db.create_all()
    print("✅ Todas las tablas fueron creadas correctamente en la base de datos.")
