from flask import jsonify, Blueprint, request
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
    
    try:
        especialidad = EspecialidadService.crear_especialidad(esp)
        return jsonify({
            "message": "Especialidad creada exitosamente",
            "data": especialidad.to_dict_simple()
        }), 201
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": "Error interno del servidor"}), 500


@especialidad_bp.route('/especialidad', methods=['GET'])
def listar_especialidades():
    try:
        result = EspecialidadService.obtener_todas()
        salida = especialidad_mapping.dump(result, many=True)
        return jsonify(salida), 200
    except Exception as e:
        return jsonify({"message": "Error interno del servidor"}), 500


@especialidad_bp.route('/especialidad/<int:eid>', methods=['GET'])
def obtener_especialidad(eid):
    obj = EspecialidadService.obtener_por_id(eid)
    if not obj:
        return jsonify({"message": "Especialidad no encontrada"}), 404

    data = especialidad_mapping.dump(obj)
    return jsonify(data), 200


@especialidad_bp.route('/especialidad/<int:eid>', methods=['PUT'])
@validate_with(EspecialidadMapping)
def actualizar_especialidad(eid):
    esp = sanitizar_especialidad_entrada(request)
    actualizado = EspecialidadService.actualizar_especialidad(eid, esp)
    
    if not actualizado:
        return jsonify({"message": "Especialidad no encontrada"}), 404

    return jsonify({
        "message": "Especialidad actualizada correctamente",
        "data": actualizado.to_dict_simple()
    }), 200
    

@especialidad_bp.route('/especialidad/<int:eid>', methods=['DELETE'])
def eliminar_especialidad(eid):
    eliminado = EspecialidadService.eliminar_especialidad(eid)

    if not eliminado:
        return jsonify({"message": "Especialidad no encontrada"}), 404

    return jsonify({
        "message": "Especialidad eliminada",
        "data": eliminado.to_dict_simple()
    }), 200