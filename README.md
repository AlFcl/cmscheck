
# CMS Detector Script

Este script ha sido creado por [alf.cl](https://github.com/alfcl) para detectar diversos Sistemas de Gestión de Contenidos (CMS) y frameworks en un sitio web. También guarda los resultados en un archivo JSON, incluyendo detalles sobre el certificado SSL/TLS del sitio web.

## Requisitos

- Python 3.x
- Paquetes: `requests`, `colorama`, `ssl`, `OpenSSL`

## Instalación

1. **Clonar el repositorio**

   ```sh
   git clone https://github.com/alfcl/cms-detector.git
   cd cms-detector
   ```

2. **Crear un entorno virtual**

   ```sh
   python3 -m venv mi_entorno
   ```

3. **Activar el entorno virtual**

   - **En macOS y Linux**:

     ```sh
     source mi_entorno/bin/activate
     ```

   - **En Windows**:

     ```sh
     mi_entorno\Scripts\activate
     ```

4. **Instalar las dependencias**

   ```sh
   pip install requests colorama
   ```

## Uso

Para ejecutar el script, utiliza el siguiente comando:

```sh
python cms.py --sitio https://ejemplo.com
```

## Funcionamiento

El script realiza las siguientes acciones:

1. **Verifica si el sitio está en línea**.
2. **Comprueba si el sitio está redirigiendo**.
3. **Obtiene los encabezados HTTP del sitio**.
4. **Escanea el sitio para detectar varios CMS y frameworks**.
5. **Guarda los resultados en un archivo JSON**, incluyendo:
   - Dominio
   - Respuesta
   - Fecha de detección
   - Si se detectó el CMS
   - Nombre del CMS (si se detectó)
   - Fecha de creación del certificado SSL/TLS
   - Fecha de vencimiento del certificado SSL/TLS

## Resultados

Los resultados se guardan en un archivo llamado `resultados.json` en el mismo directorio donde se ejecuta el script. El formato de los resultados es el siguiente:

```json
[
    {
        "dominio": "https://ejemplo.com",
        "respuesta": "[!] Detectado: WordPress en https://ejemplo.com/wp-login.php",
        "fecha": "2024-08-01 12:00:00",
        "detectado": true,
        "cms": "WordPress",
        "certificado_creacion": "2023-01-01",
        "certificado_vencimiento": "2024-01-01"
    },
    {
        "dominio": "https://ejemplo2.com",
        "respuesta": "No se detectó CMS",
        "fecha": "2024-08-01 12:00:00",
        "detectado": false,
        "cms": "No detectado",
        "certificado_creacion": "2023-01-01",
        "certificado_vencimiento": "2024-01-01"
    }
]
```

## Notas

- Asegúrate de tener acceso a internet para que el script pueda realizar las solicitudes necesarias.
- El script solo detecta los CMS y frameworks especificados en el código. Puedes agregar más verificaciones según tus necesidades.
