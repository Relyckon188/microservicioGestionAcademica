from flask import jsonify, Blueprint, request
from markupsafe import escape
from app.mapping import UniversidadMapping
from app.services.universidad_service import UniversidadService
from app.validators import validate_with
from app import cache

universidad_bp = Blueprint('universidad', __name__)

universidad_mapping = UniversidadMapping()


def sanitizar_universidad_entrada(req):
    data = universidad_mapping.load(req.get_json())
    data.nombre = escape(data.nombre)
    data.sigla = escape(data.sigla)
    return data


@universidad_bp.route('/universidad', methods=['POST'])
@validate_with(UniversidadMapping)
def crear_universidad():
    universidad = sanitizar_universidad_entrada(request)
    UniversidadService.crear_universidad(universidad)
    return jsonify({"message": "Universidad creada exitosamente"}), 201


@universidad_bp.route('/universidad', methods=['GET'])
@cache.cached(timeout=30)
def listar_universidades():
    result = UniversidadService.obtener_todas()
    return jsonify(universidad_mapping.dump(result, many=True)), 200


@universidad_bp.route('/universidad/<int:uid>', methods=['GET'])
def obtener_universidad(uid):
    obj = UniversidadService.obtener_por_id(uid)
    if not obj:
        return jsonify({"message": "Universidad no encontrada"}), 404
    return universidad_mapping.dump(obj), 200


@universidad_bp.route('/universidad/<int:uid>', methods=['PUT'])
@validate_with(UniversidadMapping)
def actualizar_universidad(uid):
    universidad = sanitizar_universidad_entrada(request)
    obj = UniversidadService.actualizar_universidad(uid, universidad)
    if not obj:
        return jsonify({"message": "Universidad no encontrada"}), 404
    return jsonify({"message": "Universidad actualizada correctamente"}), 200


@universidad_bp.route('/universidad/<int:uid>', methods=['DELETE'])
def eliminar_universidad(uid):
    eliminado = UniversidadService.eliminar_universidad(uid)
    if not eliminado:
        return jsonify({"message": "Universidad no encontrada"}), 404
    return jsonify({"message": "Universidad eliminada"}), 200
