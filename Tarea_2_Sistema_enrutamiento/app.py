from flask import Flask
from flask_cors import CORS

# Crear aplicación
app = Flask(__name__)
CORS(app)

# Importar funciones que configuran las rutas
from routes.rutas_optimizadas import registrar_rutas_optimizadas
from routes.ubicaciones import registrar_rutas_ubicaciones

# Registrar cada grupo de rutas
registrar_rutas_optimizadas(app)
registrar_rutas_ubicaciones(app)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
