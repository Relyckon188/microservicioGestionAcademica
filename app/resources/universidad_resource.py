from flask import jsonify, Blueprint, request
from app.mapping import UniversidadMapping
from app.services.universidad_service import UniversidadService
from markupsafe import escape
import json
import logging
from app.validators import validate_with
from app import cache


from typing import Dict, Any, List


universidad_bp = Blueprint('universidad', __name__)


universidad_mapping = UniversidadMapping()


@universidad_bp.route('/universidad', methods=['POST'])
def crear(universidad):
    UniversidadService.crear_universidad(universidad)
    return jsonify("Universidad creada exitosamente"), 201

def sanitizar_universidad_entrada(request):
  universidad = universidad_mapping.load(request.get_json())
  universidad.nombre = escape(universidad.nombre)
  universidad.sigla = escape(universidad.sigla)
  universidad.tipo = escape(universidad.tipo) 
  return universidad