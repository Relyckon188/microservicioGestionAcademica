from flask import jsonify, Blueprint, request, current_app
from markupsafe import escape
from app.mapping import FacultadMapping
from app.services.facultad_service import FacultadService
from app.validators import validate_with
from app import cache

facultad_bp = Blueprint('facultad', __name__)
facultad_mapping = FacultadMapping()


def sanitizar_facultad_entrada(req):
    obj = facultad_mapping.load(req.get_json())
    obj.nombre = escape(obj.nombre)
    obj.abreviatura = escape(obj.abreviatura)
    obj.directorio = escape(obj.directorio)
    obj.sigla = escape(obj.sigla)
    obj.ciudad = escape(obj.ciudad) if obj.ciudad else None
    obj.domicilio = escape(obj.domicilio) if obj.domicilio else None
    obj.telefono = escape(obj.telefono) if obj.telefono else None
    obj.contacto = escape(obj.contacto) if obj.contacto else None
    obj.email = escape(obj.email)
    return obj


@facultad_bp.route('/facultad', methods=['POST'])
@validate_with(FacultadMapping)
def crear_facultad():
    fac = sanitizar_facultad_entrada(request)
    obj = FacultadService.crear_facultad(fac)

    return jsonify({
        "message": "Facultad creada exitosamente",
        "id": current_app.hashids.encode(obj.id)
    }), 201


@facultad_bp.route('/facultad', methods=['GET'])
@cache.cached(timeout=30)
def listar_facultades():
    result = FacultadService.obtener_todas()

    salida = []
    for obj in result:
        data = facultad_mapping.dump(obj)
        data["id"] = current_app.hashids.encode(obj.id)
        salida.append(data)

    return jsonify(salida), 200


@facultad_bp.route('/facultad/<hashid>', methods=['GET'])
def obtener_facultad(hashid):
    decoded = current_app.hashids.decode(hashid)
    if not decoded:
        return jsonify({"message": "ID inválido"}), 400

    obj = FacultadService.obtener_por_id(decoded[0])
    if not obj:
        return jsonify({"message": "Facultad no encontrada"}), 404

    data = facultad_mapping.dump(obj)
    data["id"] = hashid

    return jsonify(data), 200


@facultad_bp.route('/facultad/<hashid>', methods=['PUT'])
@validate_with(FacultadMapping)
def actualizar_facultad(hashid):
    decoded = current_app.hashids.decode(hashid)
    if not decoded:
        return jsonify({"message": "ID inválido"}), 400

    fac = sanitizar_facultad_entrada(request)
    actualizado = FacultadService.actualizar_facultad(decoded[0], fac)

    if not actualizado:
        return jsonify({"message": "Facultad no encontrada"}), 404

    return jsonify({"message": "Facultad actualizada correctamente"}), 200


@facultad_bp.route('/facultad/<hashid>', methods=['DELETE'])
def eliminar_facultad(hashid):
    decoded = current_app.hashids.decode(hashid)
    if not decoded:
        return jsonify({"message": "ID inválido"}), 400

    eliminado = FacultadService.eliminar_facultad(decoded[0])
    if not eliminado:
        return jsonify({"message": "Facultad no encontrada"}), 404

    return jsonify({"message": "Facultad eliminada"}), 200
