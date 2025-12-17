def validar_dni(dni):
    if not dni.isdigit():
        raise ValueError("DNI inválido")
