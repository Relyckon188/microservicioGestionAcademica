from flask import jsonify, Blueprint, request, current_app
from markupsafe import escape
from app.mapping import UniversidadMapping
from app.services.universidad_service import UniversidadService
from app.validators import validate_with
from app import cache

universidad_bp = Blueprint('universidad', __name__)
universidad_mapping = UniversidadMapping()


def sanitizar_universidad_entrada(req):
    data = req.get_json()
    data["nombre"] = escape(data["nombre"])
    data["sigla"] = escape(data["sigla"])
    return data


@universidad_bp.route('/universidad', methods=['POST'])
@validate_with(UniversidadMapping)
def crear_universidad():
    data = sanitizar_universidad_entrada(request)
    obj = UniversidadService.crear_universidad(data)

    return jsonify({
        "message": "Universidad creada exitosamente",
        "id": current_app.hashids.encode(obj.id)
    }), 201


@universidad_bp.route('/universidad', methods=['GET'])
@cache.cached(timeout=30)
def listar_universidades():
    result = UniversidadService.obtener_todas()

    salida = []
    for obj in result:
        data = universidad_mapping.dump(obj)
        data["id"] = current_app.hashids.encode(obj.id)
        salida.append(data)

    return jsonify(salida), 200


@universidad_bp.route('/universidad/<hashid>', methods=['GET'])
def obtener_universidad(hashid):
    decoded = current_app.hashids.decode(hashid)
    if not decoded:
        return jsonify({"message": "ID inválido"}), 400

    obj = UniversidadService.obtener_por_id(decoded[0])
    if not obj:
        return jsonify({"message": "Universidad no encontrada"}), 404

    data = universidad_mapping.dump(obj)
    data["id"] = hashid

    return jsonify(data), 200


@universidad_bp.route('/universidad/<hashid>', methods=['PUT'])
@validate_with(UniversidadMapping)
def actualizar_universidad(hashid):
    decoded = current_app.hashids.decode(hashid)
    if not decoded:
        return jsonify({"message": "ID inválido"}), 400

    data = sanitizar_universidad_entrada(request)
    actualizado = UniversidadService.actualizar_universidad(decoded[0], data)

    if not actualizado:
        return jsonify({"message": "Universidad no encontrada"}), 404

    return jsonify({"message": "Universidad actualizada correctamente"}), 200


@universidad_bp.route('/universidad/<hashid>', methods=['DELETE'])
def eliminar_universidad(hashid):
    decoded = current_app.hashids.decode(hashid)
    if not decoded:
        return jsonify({"message": "ID inválido"}), 400

    eliminado = UniversidadService.eliminar_universidad(decoded[0])

    if not eliminado:
        return jsonify({"message": "Universidad no encontrada"}), 404

    return jsonify({"message": "Universidad eliminada"}), 200
