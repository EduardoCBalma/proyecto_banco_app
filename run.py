import os
from app import app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Heroku proporciona el puerto en la variable de entorno PORT
    app.run(host="0.0.0.0", port=port, debug=True)
