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
    data = sanitizar_universidad_entrada(request)
    obj = UniversidadService.crear_universidad(data)

    cache.delete_memoized(listar_universidades)

    return jsonify({
        "message": "Universidad creada exitosamente",
        "id": obj.id
    }), 201


@universidad_bp.route('/universidad', methods=['GET'])
@cache.cached(timeout=30)
def listar_universidades():
    result = UniversidadService.obtener_todas()
    salida = [universidad_mapping.dump(obj) for obj in result]
    return jsonify(salida), 200


@universidad_bp.route('/universidad/<int:uid>', methods=['GET'])
def obtener_universidad(uid):
    obj = UniversidadService.obtener_por_id(uid)

    if not obj:
        return jsonify({"message": "Universidad no encontrada"}), 404

    data = universidad_mapping.dump(obj)
    return jsonify(data), 200


@universidad_bp.route('/universidad/<int:uid>', methods=['PUT'])
@validate_with(UniversidadMapping)
def actualizar_universidad(uid):
    data = sanitizar_universidad_entrada(request)
    actualizado = UniversidadService.actualizar_universidad(uid, data)

    if not actualizado:
        return jsonify({"message": "Universidad no encontrada"}), 404

    cache.delete_memoized(listar_universidades)
    return jsonify({"message": "Universidad actualizada correctamente"}), 200


@universidad_bp.route('/universidad/<int:uid>', methods=['DELETE'])
def eliminar_universidad(uid):
    eliminado = UniversidadService.eliminar_universidad(uid)

    if not eliminado:
        return jsonify({"message": "Universidad no encontrada"}), 404

    cache.delete_memoized(listar_universidades)
    return jsonify({"message": "Universidad eliminada"}), 200