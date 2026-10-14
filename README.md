# pynmcli

Pequeño proyecto en Python para trabajar con nmcli en Linux.

El script comprueba si nmcli está instalado y, si no lo encuentra, intenta instalar NetworkManager utilizando el gestor de paquetes del sistema.
Características

- Detección de la distribución de Linux.
- Comprobación de la instalación de nmcli.
- Instalación automática de NetworkManager si es necesario.
- Mensajes de estado con colores en la terminal.

Requisitos

- Linux.
- Python 3.
- Permisos de administrador para instalar paquetes.



## Instalación:

Clonar el repositorio:

```bash
git clone https://github.com/TU-USUARIO/pynmcli.git
cd pynmcli
```

Ejecuta el instalador:

```bash
chmod +x setup.py
python setup.py
```

Para la instalación a nivel sistema:

```bash
chmod +x install.sh
./intall.sh
```

También puedes ejecutar directamente el script de Python:

```python
python3 pycli.py
```

Estructura del proyecto:

```
pynmcli/
├── install.sh
├── LICENSE
├── pycli.py
├── README.md
└── setup.py
```

Licencia

Este proyecto utiliza la licencia MIT. Consulta el archivo LICENSE para más información.

Proyecto personal con Python y trabajar con herramientas de Linux.