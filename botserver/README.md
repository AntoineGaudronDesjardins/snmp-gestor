# Gestor SNMP

# Descripción del proyecto

Este repositorio contiene el proceso que se ejecutará como gestor SNMP para la monitorizacion de la red. Utiliza la libreria pysnmp de Python para las peticiones y los traps snmp, y la libreria telepot para interactuar con la api Telegram.


# Estructura del proyecto

El archivo principal es `main.py`, y hay dos carpetas principales.

La carpeta `mibs` almacena las MIB compiladas en formato pysnmp, y dos otras carpetas : `mibs` que almacena las mibs en pleno texto (\*.mib), y compiler que contiene los scripts necesarios para compilar las mibs desde el formato \*.mib al formato pysnmp (\*.py). Los mibs compiladas permiten que se manipule directamente los nombres de las mibs y objetos en lugar de los OIDs.

La carpeta `modules` contiene dos carpetas: `utils`, que declara algunas clases fachada para usar pysnmp de manera más conveniente, y `devices`, para declarar las clases correspondientes a las operaciones SNMP disponibles en los dispositivos definidos.

La carpeta `_pysnmp_example` contiene plantillas recuperadas en la pagina web de <a href="https://pysnmp.readthedocs.io/en/latest/">pysnmp</a>. La documentacion no es siempre muy completa y a veces contiene errores.

```
gestor-snmp/
│   README.md
│   main.py
│
└── mibs/
│   │   *.py
│   │   
│   └── mibs/
│   │   └   *.mib
│   │   
│   └── compiler/
│       │   ...
│       │   loadMib.py
│       └   mibdump.py
│   
└── modules/
    │
    └── bot/
    │   └   bot.py
    │
    └── devices/
    │   └── equipoFinal/
    │   │   └   equipo.py
    │   │ 
    │   └── router/
    │   │   └   router.py
    │   │ 
    │   └── switch/
    |       |   switch.py
    │       └   switchTrapConfig.py
    │
    └── snmp/
    │   │   managedNode.py
    │   │   snmpEngine.py
    │   |   trapListener.py
    │   │   mibNode.py
    │   └   table.py
    │
    └── utils/
        │   auxiliaryClasses.py
        └   utils.py
```

# Compilación de las MIBs

Para compilar nuevas MIBs, se proporciona una carpeta llamada `compiler` en la raíz del proyecto. Si las MIBs para compilar no estan descargadas se puede actualizar la variable `mibs_to_download` del fichero `loadMib.py` con la lista de los nombres de las MIBs a descagar.

Para compilar las MIBs, se debe ejecutar el siguiente comando:

```
python3 ./mibs/compiler/mibdump.py --generate-mib-texts --mib-source "file:///absolutepathtoproject/mibs/mibs" --destination-format pysnmp --destination-directory ./mibs ./mibs/mibs/*.mib
```

Este comando compilará todas las MIB que se encuentren en la carpeta `mibs/mibs` y las almacenará en la carpeta `mibs`.

# Ejecución de la aplicación

Para ejecutar la aplicación, se debe importar las librerias necesarias ejecutando `pip install -r requirements.txt`. Una vez las dependencias importadas, se debe crear un fichero de configuracion `conf.py` a la raiz del proyecto siguiendo la plantilla `conf.template.py`. Finalment se debe ejecutar el fichero `main.py`.
