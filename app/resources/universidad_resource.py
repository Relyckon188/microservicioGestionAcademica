from flask import jsonify, Blueprint, request
from app.mapping.universidad_mapping import UniversidadMapping
from app.services.universidad_service import UniversidadService
from app.validators import validate_with

universidad_bp = Blueprint('universidad', __name__)
universidad_mapping = UniversidadMapping()


@universidad_bp.route('/universidad', methods=['POST'])
@validate_with(UniversidadMapping)
def crear_universidad():
    try:
        data = request.validated_json
        obj = UniversidadService.crear_universidad(data)
        
        return jsonify({
            "message": "Universidad creada exitosamente",
            "data": obj.to_dict_simple()
        }), 201
    except Exception as e:
        print(f"Error: {str(e)}")  # Para debug
        return jsonify({"message": "Error interno del servidor"}), 500


@universidad_bp.route('/universidad', methods=['GET'])
def listar_universidades():
    try:
        result = UniversidadService.obtener_todas()
        salida = universidad_mapping.dump(result, many=True)
        return jsonify(salida), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"message": "Error interno del servidor"}), 500


@universidad_bp.route('/universidad/<int:uid>', methods=['GET'])
def obtener_universidad(uid):
    try:
        obj = UniversidadService.obtener_por_id(uid)
        if not obj:
            return jsonify({"message": "Universidad no encontrada"}), 404
        data = universidad_mapping.dump(obj)
        return jsonify(data), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"message": "Error interno del servidor"}), 500


@universidad_bp.route('/universidad/<int:uid>', methods=['PUT'])
@validate_with(UniversidadMapping)
def actualizar_universidad(uid):
    try:
        data = request.validated_json
        actualizado = UniversidadService.actualizar_universidad(uid, data)

        if not actualizado:
            return jsonify({"message": "Universidad no encontrada"}), 404

        return jsonify({
            "message": "Universidad actualizada correctamente",
            "data": actualizado.to_dict_simple()
        }), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"message": "Error interno del servidor"}), 500


@universidad_bp.route('/universidad/<int:uid>', methods=['DELETE'])
def eliminar_universidad(uid):
    try:
        eliminado = UniversidadService.eliminar_universidad(uid)
        if not eliminado:
            return jsonify({"message": "Universidad no encontrada"}), 404

        return jsonify({
            "message": "Universidad eliminada",
            "data": eliminado.to_dict_simple()
        }), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"message": "Error interno del servidor"}), 500