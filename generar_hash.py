"""Genera el hash de una contraseña para insertarlo en la tabla usuarios.

Uso: python generar_hash.py
La contraseña se pide por teclado y no se guarda en ningún archivo.
"""
from getpass import getpass

from werkzeug.security import generate_password_hash

password = getpass('Contraseña: ')
print(generate_password_hash(password))
