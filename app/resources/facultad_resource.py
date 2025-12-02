from flask import jsonify, Blueprint, request
from markupsafe import escape
from app.mapping import FacultadMapping
from app.services.facultad_service import FacultadService
from app.validators import validate_with
from app import cache

facultad_bp = Blueprint('facultad', __name__)
facultad_mapping = FacultadMapping()


def sanitizar_facultad_entrada(req):
    obj = facultad_mapping.load(req.get_json())  # ← objeto Facultad

    # Sanitizar atributos
    obj.nombre = escape(obj.nombre)
    obj.abreviatura = escape(obj.abreviatura)
    obj.directorio = escape(obj.directorio)
    obj.sigla = escape(obj.sigla)
    obj.ciudad = escape(obj.ciudad) if obj.ciudad else None
    obj.domicilio = escape(obj.domicilio) if obj.domicilio else None
    obj.telefono = escape(obj.telefono) if obj.telefono else None
    obj.contacto = escape(obj.contacto) if obj.contacto else None
    obj.email = escape(obj.email)

    return obj   # ← devolvemos OBJETO, NO dict


@facultad_bp.route('/facultad', methods=['POST'])
@validate_with(FacultadMapping)
def crear_facultad():
    facultad_obj = sanitizar_facultad_entrada(request)
    FacultadService.crear_facultad(facultad_obj)
    return jsonify({"message": "Facultad creada exitosamente"}), 201


@facultad_bp.route('/facultad', methods=['GET'])
@cache.cached(timeout=30)
def listar_facultades():
    result = FacultadService.obtener_todas()
    return jsonify(facultad_mapping.dump(result, many=True)), 200


@facultad_bp.route('/facultad/<int:fid>', methods=['GET'])
def obtener_facultad(fid):
    obj = FacultadService.obtener_por_id(fid)
    if not obj:
        return jsonify({"message": "Facultad no encontrada"}), 404
    return facultad_mapping.dump(obj), 200


@facultad_bp.route('/facultad/<int:fid>', methods=['PUT'])
@validate_with(FacultadMapping)
def actualizar_facultad(fid):
    facultad_obj = sanitizar_facultad_entrada(request)
    actualizado = FacultadService.actualizar_facultad(fid, facultad_obj)
    if not actualizado:
        return jsonify({"message": "Facultad no encontrada"}), 404
    return jsonify({"message": "Facultad actualizada correctamente"}), 200


@facultad_bp.route('/facultad/<int:fid>', methods=['DELETE'])
def eliminar_facultad(fid):
    eliminado = FacultadService.eliminar_facultad(fid)
    if not eliminado:
        return jsonify({"message": "Facultad no encontrada"}), 404
    return jsonify({"message": "Facultad eliminada"}), 200
