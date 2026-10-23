"""Pulsarmania Cajamarca - AVANCE (semana 10): inventario, validación, búsqueda, ordenamiento y archivos.
Pendiente para la versión final: ventas (POS), fiados, compras, historial y reportes."""
import archivos as ar
import inventario as inv
import validaciones as va
from archivos import COD


def crear_usuario_inicial():
    """Crea el administrador la primera vez (guarda solo el hash de la contraseña)."""
    nombre = va.leer_texto("Nombre de usuario: ").lower()
    clave = va.leer_texto("Contraseña: ")
    if len(clave) < 4:
        print("Error: La contraseña debe tener al menos 4 caracteres")
        return False
    ar.agregar_linea("Usuarios.txt", [nombre, ar.hash_clave(clave), "administrador"])
    print("Usuario administrador creado")
    return True


def iniciar_sesion():
    """Devuelve (usuario, rol) o None."""
    nombre = va.leer_texto("Usuario: ").lower()
    clave = ar.hash_clave(va.leer_texto("Contraseña: "))
    for linea in ar.leer_lineas("Usuarios.txt"):
        u = linea.split(ar.SEP)
        if u[0] == nombre and u[1] == clave:
            print(f"Inicio de sesión exitoso. Rol: {u[2]}")
            return u[0], u[2]
    print("Error: Usuario o contraseña incorrectos")
    return None


def menu_inicial():
    while True:
        print("\n=== PULSARMANIA CAJAMARCA (AVANCE) ===\n1. Iniciar sesión\n2. Crear usuario inicial\n0. Salir")
        op = va.leer_opcion("Opción: ", 0, 2)
        if op == 0:
            return None
        if op == 2:
            if ar.leer_lineas("Usuarios.txt"):
                print("Ya existe un usuario. Inicie sesión.")
            else:
                crear_usuario_inicial()
        else:
            sesion = iniciar_sesion()
            if sesion:
                return sesion


def menu_principal(usuario, rol):
    while True:
        productos = ar.cargar_productos()
        print(f"\n=== MENÚ PRINCIPAL ({usuario} - {rol}) ===")
        print("1. Ver inventario (ordenado)\n2. Buscar producto\n3. Agregar producto\n4. Modificar precio\n0. Cerrar sesión")
        op = va.leer_opcion("Opción: ", 0, 4)
        if op == 0:
            return
        if op == 1:
            inv.ver_inventario(productos, rol)
        elif op == 2:
            print("Buscar por: 1) Código  2) Nombre / marca / moto")
            if va.leer_opcion("Opción: ", 1, 2) == 1:
                orden = inv.ordenar(productos, COD)
                pos = inv.buscar_binario(orden, va.leer_texto("Código: "))
                inv.mostrar_tabla([orden[pos]] if pos != -1 else [], rol)
            else:
                inv.mostrar_tabla(inv.buscar_texto(productos, va.leer_texto("Texto a buscar: ")), rol)
        elif op == 3:
            inv.agregar_producto(productos)
        elif op == 4:
            inv.modificar_producto(productos)


def main():
    while True:
        sesion = menu_inicial()
        if sesion is None:
            print("Saliendo del sistema...")
            break
        menu_principal(*sesion)


if __name__ == "__main__":
    main()
