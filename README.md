# pynmcli

A Python project for working with nmcli on Linux.

The script checks whether nmcli is installed and, if it isn't found, attempts to install NetworkManager using the system's package manager.
Features

- Detection of the Linux distribution.
- Checking for the installation of nmcli.
- Automatic installation of NetworkManager if necessary.
- Color-coded status messages in the terminal.

Requirements:

- Linux.
- Python 3.
- Administrator permissions to install packages.



## Installation:

Clone the repository:

```bash
git clone https://github.com/DcastrGD/pynmcli.git
cd pynmcli
```

Run the installer:

```bash
chmod +x setup.py
python setup.py
```

For system-wide installation:

```bash
chmod +x install.sh
./intall.sh
```

You can also run the Python script directly:

```python
python3 pycli.py
```

Project Structure:

```
pynmcli/
├── install.sh
├── LICENSE
├── pycli.py
├── README.md
└── setup.py
```

License

This project is licensed under the MIT License. See the LICENSE file for more information.
