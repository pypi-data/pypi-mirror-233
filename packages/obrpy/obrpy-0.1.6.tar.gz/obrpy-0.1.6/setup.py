import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

VERSION = '0.1.6' #Muy importante, deberéis ir cambiando la versión de vuestra librería según incluyáis nuevas funcionalidades
PACKAGE_NAME = 'obrpy' #Debe coincidir con el nombre de la carpeta 
AUTHOR = 'Andres Pedraza Rodriguez' #Modificar con vuestros datos
AUTHOR_EMAIL = 'a.pedraza@upm.es' #Modificar con vuestros datos
URL = 'https://github.com/temisAP' #Modificar con vuestros datos

LICENSE = 'MIT' #Tipo de licencia
DESCRIPTION = "This library is aimed for using Luna's OBR-4600 with Python." #Descripción corta
LONG_DESCRIPTION = (HERE / "readme.md").read_text(encoding='utf-8') #Referencia al documento README con una descripción más elaborada
LONG_DESC_TYPE = "text/markdown"


# Paquetes necesarios para que funcione la libreía. Se instalarán a la vez si no lo tuvieras ya instalado
# Path to the requirements.txt file
requirements_path = "requirements.txt"

# Initialize the INSTALL_REQUIRES list
INSTALL_REQUIRES = []

# Read the requirements.txt file
with open(requirements_path, "r", encoding='utf-16') as file:
    requirements = file.read().splitlines()

#print([r for r in requirements])

# Exclude "cupy" from the requirements and add the rest to INSTALL_REQUIRES
for requirement in requirements:
    
    # Split the requirement at the "==" sign and extract the library name
    library_name = requirement.split("==")[0].strip()
    if library_name != "cupy":
        INSTALL_REQUIRES.append(library_name)


setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    license=LICENSE,
    packages=find_packages(),
    package_data={'obrpy':['UTILS/*','ANALYSIS/*','obrsdk/*','signal/*','ZERO_LAYERS/*']},
    include_package_data=True
)