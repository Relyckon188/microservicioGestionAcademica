from flask import jsonify, Blueprint, request, current_app
from markupsafe import escape
from app.mapping import EspecialidadMapping
from app.services.especialidad_service import EspecialidadService
from app.validators import validate_with
from app import cache

especialidad_bp = Blueprint('especialidad', __name__)
especialidad_mapping = EspecialidadMapping()


def sanitizar_especialidad_entrada(req):
    data = especialidad_mapping.load(req.get_json())
    data.nombre = escape(data.nombre)
    data.letra = escape(data.letra)
    data.observacion = escape(data.observacion) if data.observacion else None
    return data


@especialidad_bp.route('/especialidad', methods=['POST'])
@validate_with(EspecialidadMapping)
def crear_especialidad():
    esp = sanitizar_especialidad_entrada(request)
    obj = EspecialidadService.crear_especialidad(esp)

    return jsonify({
        "message": "Especialidad creada exitosamente",
        "id": current_app.hashids.encode(obj.id)
    }), 201


@especialidad_bp.route('/especialidad', methods=['GET'])
@cache.cached(timeout=30)
def listar_especialidades():
    result = EspecialidadService.obtener_todas()

    salida = []
    for obj in result:
        data = especialidad_mapping.dump(obj)
        data["id"] = current_app.hashids.encode(obj.id)
        salida.append(data)

    return jsonify(salida), 200


@especialidad_bp.route('/especialidad/<hashid>', methods=['GET'])
def obtener_especialidad(hashid):
    decoded = current_app.hashids.decode(hashid)
    if not decoded:
        return jsonify({"message": "ID inválido"}), 400

    obj = EspecialidadService.obtener_por_id(decoded[0])
    if not obj:
        return jsonify({"message": "Especialidad no encontrada"}), 404

    data = especialidad_mapping.dump(obj)
    data["id"] = hashid

    return jsonify(data), 200


@especialidad_bp.route('/especialidad/<hashid>', methods=['PUT'])
@validate_with(EspecialidadMapping)
def actualizar_especialidad(hashid):
    decoded = current_app.hashids.decode(hashid)
    if not decoded:
        return jsonify({"message": "ID inválido"}), 400

    esp = sanitizar_especialidad_entrada(request)
    actualizado = EspecialidadService.actualizar_especialidad(decoded[0], esp)

    if not actualizado:
        return jsonify({"message": "Especialidad no encontrada"}), 404

    return jsonify({"message": "Especialidad actualizada correctamente"}), 200


@especialidad_bp.route('/especialidad/<hashid>', methods=['DELETE'])
def eliminar_especialidad(hashid):
    decoded = current_app.hashids.decode(hashid)
    if not decoded:
        return jsonify({"message": "ID inválido"}), 400

    eliminado = EspecialidadService.eliminar_especialidad(decoded[0])

    if not eliminado:
        return jsonify({"message": "Especialidad no encontrada"}), 404

    return jsonify({"message": "Especialidad eliminada"}), 200
