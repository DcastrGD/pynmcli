#!/bin/bash

if [ "$(whoami)" = "root" ]; then
    echo "Eres root."
else
    echo "No eres root."
    exit 1
fi

function Install_pycli {

    read -p "[+] ¿Deseas instalar las herramientas de desarrollo? [S/n]: " respuesta

    if [[ "$respuesta" =~ ^[Ss]$ ]] || [ -z "$respuesta" ]; then
        echo "[+] Instalando el programa..."
        cp pycli.py /usr/local/bin/pycli.py
        chmod +x /usr/local/bin/pycli.py
        rehash
        
        sleep 3
        echo "[+] Instalación terminada..."
    else
        echo "[-] Instalación cancelada..."
    fi

}


Install_pycli
