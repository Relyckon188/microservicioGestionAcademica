from flask import jsonify, Blueprint, request
from markupsafe import escape
from app.mapping import FacultadMapping
from app.services.facultad_service import FacultadService
from app.validators import validate_with

facultad_bp = Blueprint('facultad', __name__)
facultad_mapping = FacultadMapping()


def sanitizar_facultad_entrada(req):
    data = facultad_mapping.load(req.get_json())

    data.nombre = escape(data.nombre)
    data.abreviatura = escape(data.abreviatura)
    data.directorio = escape(data.directorio)
    data.sigla = escape(data.sigla)

    data.ciudad = escape(data.ciudad) if data.ciudad else None
    data.domicilio = escape(data.domicilio) if data.domicilio else None
    data.telefono = escape(data.telefono) if data.telefono else None
    data.contacto = escape(data.contacto) if data.contacto else None
    data.email = escape(data.email) if data.email else None

    return data


@facultad_bp.route('/facultad', methods=['POST'])
@validate_with(FacultadMapping)
def crear_facultad():
    try:
        fac = sanitizar_facultad_entrada(request)
        obj = FacultadService.crear_facultad(fac)
        
        return jsonify({
            "message": "Facultad creada exitosamente",
            "data": obj.to_dict_simple()
        }), 201
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": "Error interno del servidor"}), 500


@facultad_bp.route('/facultad', methods=['GET'])
def listar_facultades():
    try:
        result = FacultadService.obtener_todas()
        salida = facultad_mapping.dump(result, many=True)
        return jsonify(salida), 200
    except Exception as e:
        return jsonify({"message": "Error interno del servidor"}), 500


@facultad_bp.route('/facultad/<int:fid>', methods=['GET'])
def obtener_facultad(fid):
    obj = FacultadService.obtener_por_id(fid)
    if not obj:
        return jsonify({"message": "Facultad no encontrada"}), 404

    data = facultad_mapping.dump(obj)
    return jsonify(data), 200


@facultad_bp.route('/facultad/<int:fid>', methods=['PUT'])
@validate_with(FacultadMapping)
def actualizar_facultad(fid):
    try:
        fac = sanitizar_facultad_entrada(request)
        actualizado = FacultadService.actualizar_facultad(fid, fac)

        if not actualizado:
            return jsonify({"message": "Facultad no encontrada"}), 404

        return jsonify({
            "message": "Facultad actualizada correctamente",
            "data": actualizado.to_dict_simple()
        }), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": "Error interno del servidor"}), 500


@facultad_bp.route('/facultad/<int:fid>', methods=['DELETE'])
def eliminar_facultad(fid):
    eliminado = FacultadService.eliminar_facultad(fid)

    if not eliminado:
        return jsonify({"message": "Facultad no encontrada"}), 404

    return jsonify({
        "message": "Facultad eliminada",
        "data": eliminado.to_dict_simple()
    }), 200