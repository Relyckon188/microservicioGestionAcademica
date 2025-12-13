from flask import jsonify, Blueprint, request, current_app
from markupsafe import escape
from app.mapping import EspecialidadMapping
from app.services.especialidad_service import EspecialidadService
from app.validators import validate_with

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
    especialidad = EspecialidadService.crear_especialidad(esp)

    # devolver id numerico (no hashid)
    return jsonify({
        "message": "Especialidad creada exitosamente",
        "data": {
            "id": especialidad.id,
            "especialidad": especialidad.nombre,
            "facultad": especialidad.facultad.nombre,
            "universidad": especialidad.facultad.universidad.nombre
        }
    }), 201


@especialidad_bp.route('/especialidad', methods=['GET'])
def listar_especialidades():
    result = EspecialidadService.obtener_todas()

    salida = especialidad_mapping.dump(result, many=True)
    
    return jsonify(salida), 200


@especialidad_bp.route('/especialidad/<int:eid>', methods=['GET'])
def obtener_especialidad(eid):
    #aplicar cache por id
    cache_key = key = f"especilidad_{eid}"
    cached = current_app.extensions['cache'].get(cache_key)
    if cached:
        return jsonify({cached}), 200

    obj = EspecialidadService.obtener_por_id(eid)
    if not obj:
        return jsonify({"message": "Especialidad no encontrada"}), 404

    data = especialidad_mapping.dump(obj)
    data["id"] = obj.id

    # guardar en cache (timeout 60 seg)
    current_app.extensions['cache'].set(cache_key, data, timeout=60)
    
    return jsonify(data), 200


@especialidad_bp.route('/especialidad/<int:eid>', methods=['PUT'])
@validate_with(EspecialidadMapping)
def actualizar_especialidad(eid):
    esp = sanitizar_especialidad_entrada(request)
    actualizado = EspecialidadService.actualizar_especialidaddes(eid, esp)
    
    if not actualizado:
        return jsonify({"message": "Especialidad no encontrada"}), 404

    cache_key = f"especialidad_{eid}"
    current_app.extensions1['cache'].delete(cache_key)

    return jsonify({"message": "Especialidad actualizada correctamente"}), 200


@especialidad_bp.route('/especialidad/<int:eid>', methods=['DELETE'])
def eliminar_especialidad(eid):
    eliminado = EspecialidadService.eliminar_especialidad(eid)

    if not eliminado:
        return jsonify({"message": "Especialidad no encontrada"}), 404
    
    # invalidar cache
    cache_key = f"especialidad_{eid}"
    current_app.extensions['cache'].delete(cache_key)

    return jsonify({"message": "Especialidad eliminada"}), 200
