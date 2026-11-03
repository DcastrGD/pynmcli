#!/usr/bin/env python3

import subprocess
import ipaddress

ROJO = "\033[91m"
VERDE = "\033[92m"
AMARILLO = "\033[93m"
AZUL = "\033[94m"
RESET = "\033[0m"


class NMCLI_CONFIGS:

    def __init__(self):
        self.name_conexion = ""

    # Ejecutar comandos de nmcli
    def ejecutar_comando(self, args):
        resultado = subprocess.run(
            ["nmcli"] + args,
            capture_output=True,
            text=True
        )

        if resultado.returncode != 0:
            print(f"{ROJO}Error: {resultado.stderr.strip()}{RESET}")
            return False

        if resultado.stdout.strip():
            print(resultado.stdout.strip())

        return True

    # Limpiar la terminal
    def limpiar_terminal(self):
        subprocess.run(["clear"])

    # Mostrar y eliminar conexiones
    def delete_interface(self):
        self.limpiar_terminal()

        print(f"{AZUL}Conexiones disponibles:{RESET}\n")

        if not self.ejecutar_comando(["con", "show"]):
            return

        nombre = input(
            f"\n{AZUL}[*]{RESET} Nombre de la conexión a eliminar "
            "(ENTER para saltar): "
        ).strip()

        if nombre == "":
            return

        confirmar = input(
            f"{AMARILLO}¿Quieres eliminar {nombre}? (s/n): {RESET}"
        ).strip().lower()

        if confirmar == "s":
            self.ejecutar_comando([
                "con", "delete", "id", nombre
            ])

    # Seleccionar una conexión existente
    def show_interface(self):
        self.limpiar_terminal()

        print(f"{AZUL}Conexiones disponibles:{RESET}\n")

        if not self.ejecutar_comando(["con", "show"]):
            return

        nombre = input(
            f"\n{AZUL}[*]{RESET} Selecciona una conexión "
            "(ENTER para crear una nueva): "
        ).strip()

        if nombre == "":
            self.name_conexion = ""
            return

        resultado = subprocess.run(
            ["nmcli", "-g", "NAME", "con", "show"],
            capture_output=True,
            text=True
        )

        conexiones = resultado.stdout.splitlines()

        if resultado.returncode != 0 or nombre not in conexiones:
            print(f"{ROJO}La conexión no existe.{RESET}")
            self.name_conexion = ""
            return

        self.name_conexion = nombre

    # Crear un perfil nuevo
    def add_profiles(self):
        print(f"\n{VERDE}Crear un nuevo perfil{RESET}")

        nombre = input("Nombre de la conexión: ").strip()

        if not nombre:
            print(f"{ROJO}El nombre es obligatorio.{RESET}")
            return

        tipo = input(
            "Tipo de interfaz (ethernet, wifi) [ethernet]: "
        ).strip().lower()

        if tipo == "":
            tipo = "ethernet"

        ifname = input(
            "Nombre del dispositivo (ej. enp0s3): "
        ).strip()

        if ifname == "":
            print(f"{ROJO}El dispositivo es obligatorio.{RESET}")
            return

        correcto = self.ejecutar_comando([
            "con", "add",
            "con-name", nombre,
            "type", tipo,
            "ifname", ifname
        ])

        if correcto:
            self.name_conexion = nombre
            print(f"{VERDE}Perfil creado correctamente.{RESET}")

    # Modificar la configuración IPv4
    def modify_interface(self):

        if not self.name_conexion:
            print(f"{ROJO}No hay ninguna conexión seleccionada.{RESET}")
            return

        nombre = self.name_conexion

        print(f"\n{VERDE}Configurando la conexión: {nombre}{RESET}")

        print("\nMétodo IPv4:")
        print("1. Manual (IP estática)")
        print("2. Auto (DHCP)")
        print("3. Mantener el método actual")

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            metodo = "manual"
        elif opcion == "2":
            metodo = "auto"
        elif opcion == "3" or opcion == "":
            metodo = ""
        else:
            print(f"{ROJO}Opción no válida.{RESET}")
            return

        ip = ""
        gateway = ""
        dns = ""

        # Pedir los datos si se va a utilizar IP manual
        if metodo == "manual":

            ip = input(
                "Dirección IP con prefijo (ej. 192.168.1.20/24): "
            ).strip()

            try:
                ipaddress.IPv4Interface(ip)
            except ValueError:
                print(f"{ROJO}La dirección IP no es válida.{RESET}")
                return

            gateway = input(
                "Puerta de enlace (ENTER para omitir): "
            ).strip()

            if gateway:
                try:
                    ipaddress.IPv4Address(gateway)
                except ValueError:
                    print(f"{ROJO}La puerta de enlace no es válida.{RESET}")
                    return

            dns = input(
                "DNS (ENTER para omitir; varios separados por comas): "
            ).strip()

            if dns:
                try:
                    dns = ",".join(
                        str(ipaddress.IPv4Address(x.strip()))
                        for x in dns.split(",")
                    )
                except ValueError:
                    print(f"{ROJO}El DNS no es válido.{RESET}")
                    return

        # Configurar primero la dirección IP
        if metodo == "manual":

            if not self.ejecutar_comando([
                "con", "modify", nombre,
                "ipv4.addresses", ip
            ]):
                return

            # Configurar la puerta de enlace
            if not self.ejecutar_comando([
                "con", "modify", nombre,
                "ipv4.gateway", gateway
            ]):
                return

            # Configurar el DNS
            if not self.ejecutar_comando([
                "con", "modify", nombre,
                "ipv4.dns", dns
            ]):
                return

        # Si se elige DHCP, eliminar los valores estáticos
        elif metodo == "auto":

            if not self.ejecutar_comando([
                "con", "modify", nombre,
                "ipv4.addresses", ""
            ]):
                return

            if not self.ejecutar_comando([
                "con", "modify", nombre,
                "ipv4.gateway", ""
            ]):
                return

            if not self.ejecutar_comando([
                "con", "modify", nombre,
                "ipv4.dns", ""
            ]):
                return

        # Configurar el método SIEMPRE al final
        if metodo:
            if not self.ejecutar_comando([
                "con", "modify", nombre,
                "ipv4.method", metodo
            ]):
                return

        print(f"\n{VERDE}Configuración guardada.{RESET}")

        activar = input(
            "¿Quieres activar la conexión ahora? (s/n): "
        ).strip().lower()

        if activar == "s":
            self.ejecutar_comando([
                "con", "up", "id", nombre
            ])


# Programa principal
def main():

    nmcli = NMCLI_CONFIGS()

    # Eliminar una conexión o saltar
    nmcli.delete_interface()

    # Seleccionar una conexión existente
    nmcli.show_interface()

    # Si no se ha seleccionado ninguna, crear un perfil
    if nmcli.name_conexion == "":

        print(
            f"\n{AMARILLO}No has seleccionado una conexión existente."
            f"{RESET}"
        )

        crear = input(
            "¿Quieres crear un perfil nuevo? (s/n): "
        ).strip().lower()

        if crear != "s":
            print("Saliendo del programa.")
            return

        nmcli.add_profiles()

    # Modificar la conexión seleccionada o creada
    if nmcli.name_conexion:
        nmcli.modify_interface()


if __name__ == "__main__":
    main()