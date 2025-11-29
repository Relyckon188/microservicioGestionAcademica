from flask import jsonify, Blueprint, request
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
    especialidad = sanitizar_especialidad_entrada(request)
    EspecialidadService.crear_especialidad(especialidad)
    return jsonify({"message": "Especialidad creada exitosamente"}), 201


@especialidad_bp.route('/especialidad', methods=['GET'])
@cache.cached(timeout=30)
def listar_especialidades():
    result = EspecialidadService.obtener_todas()
    return jsonify(especialidad_mapping.dump(result, many=True)), 200


@especialidad_bp.route('/especialidad/<int:eid>', methods=['GET'])
def obtener_especialidad(eid):
    obj = EspecialidadService.obtener_por_id(eid)
    if not obj:
        return jsonify({"message": "Especialidad no encontrada"}), 404
    return especialidad_mapping.dump(obj), 200


@especialidad_bp.route('/especialidad/<int:eid>', methods=['PUT'])
@validate_with(EspecialidadMapping)
def actualizar_especialidad(eid):
    especialidad = sanitizar_especialidad_entrada(request)
    obj = EspecialidadService.actualizar_especialidad(eid, especialidad)
    if not obj:
        return jsonify({"message": "Especialidad no encontrada"}), 404
    return jsonify({"message": "Especialidad actualizada correctamente"}), 200


@especialidad_bp.route('/especialidad/<int:eid>', methods=['DELETE'])
def eliminar_especialidad(eid):
    eliminado = EspecialidadService.eliminar_especialidad(eid)
    if not eliminado:
        return jsonify({"message": "Especialidad no encontrada"}), 404
    return jsonify({"message": "Especialidad eliminada"}), 200
