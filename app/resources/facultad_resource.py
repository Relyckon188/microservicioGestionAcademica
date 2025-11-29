from flask import jsonify, Blueprint, request
from markupsafe import escape
from app.mapping import FacultadMapping
from app.services.facultad_service import FacultadService
from app.validators import validate_with
from app import cache

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
    data.email = escape(data.email)

    return data


@facultad_bp.route('/facultad', methods=['POST'])
@validate_with(FacultadMapping)
def crear_facultad():
    facultad = sanitizar_facultad_entrada(request)
    FacultadService.crear_facultad(facultad)
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
    facultad = sanitizar_facultad_entrada(request)
    obj = FacultadService.actualizar_facultad(fid, facultad)
    if not obj:
        return jsonify({"message": "Facultad no encontrada"}), 404
    return jsonify({"message": "Facultad actualizada correctamente"}), 200


@facultad_bp.route('/facultad/<int:fid>', methods=['DELETE'])
def eliminar_facultad(fid):
    eliminado = FacultadService.eliminar_facultad(fid)
    if not eliminado:
        return jsonify({"message": "Facultad no encontrada"}), 404
    return jsonify({"message": "Facultad eliminada"}), 200
