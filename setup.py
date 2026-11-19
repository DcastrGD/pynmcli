import os
import shutil
import subprocess
import sys

# Colores
ROJO = "\033[91m"
VERDE = "\033[92m"
AMARILLO = "\033[93m"
AZUL = "\033[94m"
RESET = "\033[0m"


def detectar_distro():
    try:
        with open("/etc/os-release", "r") as archivo:
            for linea in archivo:
                if linea.startswith("PRETTY_NAME="):
                    distro = linea.split("=", 1)[1].strip().strip('"')
                    print(f"{AZUL}[*] Distro: {distro}{RESET}")
                    return distro

    except FileNotFoundError:
        print(f"{ROJO}[!] No se pudo detectar la distro.{RESET}")

    return "Desconocida"


def instalar_nmcli():
    if shutil.which("apt-get"):
        comando = ["apt-get", "install", "-y", "network-manager"]
    elif shutil.which("dnf"):
        comando = ["dnf", "install", "-y", "NetworkManager"]
    elif shutil.which("pacman"):
        comando = ["pacman", "-S", "--noconfirm", "networkmanager"]
    elif shutil.which("zypper"):
        comando = ["zypper", "--non-interactive", "install", "NetworkManager"]
    elif shutil.which("apk"):
        comando = ["apk", "add", "networkmanager"]
    else:
        print(f"{ROJO}[!] Gestor de paquetes no compatible.{RESET}")
        return False

    # Comprobar permisos
    if os.geteuid() != 0:
        if not shutil.which("sudo"):
            print(f"{ROJO}[!] Necesitas permisos de root.{RESET}")
            return False

        comando.insert(0, "sudo")

    print(f"{AMARILLO}[*] Instalando NetworkManager...{RESET}")

    try:
        subprocess.run(comando, check=True)

        if shutil.which("nmcli"):
            print(f"{VERDE}[+] Instalado correctamente.{RESET}")
            return True

    except subprocess.CalledProcessError:
        print(f"{ROJO}[!] Error durante la instalación.{RESET}")

    return False


def comprobar_nmcli():
    if shutil.which("nmcli"):
        print(f"{VERDE}[+] nmcli ya está instalado.{RESET}")
        return True

    print(f"{AMARILLO}[-] nmcli no está instalado.{RESET}")
    return instalar_nmcli()


if __name__ == "__main__":
    if not sys.platform.startswith("linux"):
        print(f"{ROJO}[!] Este script solo funciona en Linux.{RESET}")
        sys.exit(1)

    detectar_distro()

    if not comprobar_nmcli():
        sys.exit(1)
