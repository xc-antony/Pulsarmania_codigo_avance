"""Módulo de persistencia: lectura y escritura de archivos .txt (separador '|')."""
import hashlib
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datos")
SEP = "|"

# Posiciones de cada campo en un registro de producto (arreglo bidimensional)
COD, NOM, CAT, MARCA, MOTO, UNI, PCOMPRA, PVENTA, PMEC, STOCK, SMIN, UBIC, PROV = range(13)


def ruta(nombre):
    return os.path.join(DATA_DIR, nombre)


def leer_lineas(nombre):
    """Devuelve las líneas del archivo; si no existe lo crea (FileNotFoundError)."""
    try:
        with open(ruta(nombre), "r", encoding="utf-8") as f:
            return [l.rstrip("\n") for l in f if l.strip() != ""]
    except FileNotFoundError:
        os.makedirs(DATA_DIR, exist_ok=True)
        open(ruta(nombre), "w", encoding="utf-8").close()
        return []


def agregar_linea(nombre, campos):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(ruta(nombre), "a", encoding="utf-8") as f:
        f.write(SEP.join(str(c) for c in campos) + "\n")


def reescribir(nombre, filas):
    with open(ruta(nombre), "w", encoding="utf-8") as f:
        for fila in filas:
            f.write(SEP.join(str(c) for c in fila) + "\n")


def cargar_productos():
    """Lee Productos.txt y devuelve una lista de registros con tipos convertidos."""
    productos = []
    for linea in leer_lineas("Productos.txt"):
        c = linea.split(SEP)
        if len(c) != 13:
            continue  # línea dañada: se ignora
        try:
            c[PCOMPRA], c[PVENTA], c[PMEC] = float(c[PCOMPRA]), float(c[PVENTA]), float(c[PMEC])
            c[STOCK], c[SMIN] = float(c[STOCK]), int(c[SMIN])
        except ValueError:
            continue
        productos.append(c)
    return productos


def guardar_productos(productos):
    reescribir("Productos.txt", productos)


def hash_clave(clave):
    """Guarda la contraseña como hash SHA-256 (no en texto plano)."""
    return hashlib.sha256(clave.encode("utf-8")).hexdigest()
