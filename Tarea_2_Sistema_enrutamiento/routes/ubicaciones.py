from flask import jsonify
import numpy as np
from services.data_loader import cargar_datos


_, _, ubicaciones_df, _, _ = cargar_datos()

def registrar_rutas_ubicaciones(app):
    """Registra las rutas relacionadas con ubicaciones."""

    @app.route("/ubicaciones", methods=["GET"])
    def obtener_ubicaciones():
        data = ubicaciones_df.replace({np.nan: None}).to_dict(orient="records")
        return jsonify(data)
