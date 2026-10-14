#!/usr/bin/env python3

import subprocess

ROJO = "\033[91m"
VERDE = "\033[92m"
AMARILLO = "\033[93m"
AZUL = "\033[94m"
RESET = "\033[0m"

class NMCLI_CONFIGS:

    def __init__(self):
        
        self.name_conexion = []

    def delete_interface(self):
        show_interface = subprocess.run(["nmcli con show"], shell=True, capture_output=True, text=True)
        print(show_interface.stdout)

        print(f"{VERDE}[+]{RESET} Saltar eliminación de la Interfaz (ENTER)")
        delete_interface = input(f"{AZUL}[*]{RESET} Escribe el nombre de la interfaz a eliminar (NAME): ")

        delete = subprocess.run([f"nmcli con delete {delete_interface}"], shell=True, capture_output=True, text=True)
        print(delete.stdout)

        return delete

    def show_interface(self):

        clear = subprocess.run(["clear"], shell=True, capture_output=True, text=True)
        print(clear.stdout)
        
        delete = subprocess.run(["nmcli con show"], shell=True, capture_output=True, text=True)
        print(delete.stdout)

        print(f"{VERDE}[+]{RESET} Para configurar un nuevo perfil de interfaz (ENTER)")
        name = input(f"{AZUL}[*]{RESET} Seleccione la conexión a modificar (NAME): ")

        
        self.name_conexion.append(name)

        return self.name_conexion 
       

    def add_profiles(self):

        name = None
        tipo = None
        ifname = None
        
        try:
            while name is None:
                entrada = input("Escriba el nombre de la conexión: ")
                if entrada != "":
                    name = entrada

            while tipo is None:
                entrada = input("Tipo de la interfaz (ethernet): ")
                if entrada != "":
                    tipo = entrada

            while ifname is None:
                entrada = input("Nombre de la interfaz (enp0sX): ")
                if entrada != "":
                    ifname = entrada

            add_profiles = subprocess.run(
                [
                    "nmcli", "con", "add",
                    "con-name", name,
                    "type", tipo,
                    "ifname", ifname
                ],
                capture_output=True,
                text=True
            )

        except Exception as e:
            print(f"Error: {e}")


    def modify_interface(self):
        
        ip = str(input("Escriba la ip X.X.X.X/XX: "))

        if ip != "":
             modify_interface_ip = subprocess.run([f"nmcli con modify {self.name_conexion} ipv4.address {ip}"], shell=True, capture_output=True, text=True)  
        else:
             modify_interface_ip = subprocess.run([f"nmcli con modify {self.name_conexion} ipv4.address {ip}"], shell=True, capture_output=True, text=True)
             print(modify_interface_ip.stdout)

        gateway = str(input("Esciba la puerta de enlace: "))
        
        if gateway != "":
            modify_interface_gateway = subprocess.run([f"nmcli con modify  {self.name_conexion} ipv4.gateway {gateway}"], shell=True, capture_output=True, text=True)
        else:
            modify_interface_gateway = subprocess.run([f"nmcli con modify  {self.name_conexion} ipv4.gateway {gateway}"], shell=True, capture_output=True, text=True)
            print(modify_interface_gateway.stdout)

    
        dns = str(input("Escriba el dns: "))
        
        if dns != "":
            modify_interface_dns = subprocess.run([f"nmcli con modify {self.name_conexion} ipv4.dns {dns}"], shell=True, capture_output=True, text=True)
        else:
            modify_interface_dns = subprocess.run([f"nmcli con modify {self.name_conexion} ipv4.dns {dns}"], shell=True, capture_output=True, text=True)
            print(modify_interface_dns.stdout)

       
        method = input("Escriba el método que vas a usar (manual, auto): ")    
            
        if method != "":
            modify_interface_method = subprocess.run([f"nmcli con modify {self.name_conexion} ipv4.method {method}"], shell=True, capture_output=True, text=True)
        else: 
             modify_interface_method = subprocess.run([f"nmcli con modify {self.name_conexion} ipv4.method {method}"], shell=True, capture_output=True, text=True)
             print(modify_interface_method.stdout)
               
        
        modify_interface_down_up = subprocess.run([f"nmcli con modify up {self.name_conexion}"], shell=True, capture_output=True, text=True)
        print(modify_interface_down_up.stdout)



NMCLI = NMCLI_CONFIGS()

NMCLI.delete_interface()
    
NMCLI.show_interface()

if not NMCLI.name_conexion or NMCLI.name_conexion[0] == "":

    clear = subprocess.run(["clear"], shell=True, capture_output=True, text=True)
    print(clear.stdout)

    print(f"{AMARILLO}[-]{RESET} No seleccionaste ninguna interfaz existente...")
    print(f"{VERDE}[+]{RESET} Creación de nuevo perfil de interfaz:\n ")
    NMCLI.add_profiles()

    print(f"\n{VERDE}[+]{RESET} Pasando a modificar la nueva conexión:")
    NMCLI.modify_interface()
else:
    clear = subprocess.run(["clear"], shell=True, capture_output=True, text=True)
    print(clear.stdout)
    # Si el usuario escribió una interfaz válida (ej. enp0s8)
    print(f"{VERDE}[+]{RESET} Pasando a modificar la interfaz seleccionada...")
    NMCLI.modify_interface()
