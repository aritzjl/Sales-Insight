# **Configuración de la Herramienta**

Bienvenido a la guía de configuración de la herramienta. Siga detenidamente los pasos a continuación para configurar correctamente el entorno y las credenciales necesarias para el funcionamiento adecuado de la herramienta.

## **Funcionalidad de la Herramienta**

La herramienta está diseñada para facilitar el entrenamiento de vendedores telefónicos. El proceso se lleva a cabo de la siguiente manera:

1. **Descarga de Llamadas:** Cuando un vendedor finaliza una llamada, la herramienta descarga automáticamente las nuevas llamadas.
2. **Transcripción con IA:** Las llamadas descargadas se transcriben utilizando inteligencia artificial (IA), lo que permite obtener un texto legible a partir de las grabaciones de las llamadas.
3. **Generación de Reportes:** La herramienta utiliza otra IA para analizar la transcripción de la llamada junto con el guion que el vendedor debía seguir. Con esta información, se genera un reporte que compara la llamada con el guion, identificando áreas de mejora y destacando el desempeño del vendedor.
4. **Envío de Guiones por Email:** Finalmente, la herramienta envía el guion generado por correo electrónico al vendedor, proporcionando retroalimentación inmediata y facilitando su proceso de aprendizaje y mejora continua.

## **Configuración de la Base de Datos**

Para configurar la conexión a la base de datos, siga estos pasos:

1. Abra el archivo **`connect.py`** en un editor de texto.
2. Edite los datos de conexión con su base de datos MariaDB:

```python
import mariadb

def conectar():
    conn = mariadb.connect(
        user="usuario",            # Reemplace "usuario" con el nombre de usuario de su base de datos
        password="contraseña",     # Reemplace "contraseña" con la contraseña de su base de datos
        host="localhost",          # Reemplace "localhost" si la base de datos está en otro servidor
        port=3306,                 # Reemplace 3306 con el puerto de su base de datos
        database="GPTSales"        # Reemplace "GPTSales" con el nombre de su base de datos
    )
    return conn

```

3. Guarde los cambios realizados en el archivo.
4. Ejecute `createddbb.py`para que se creen las tablas necesarias en la base de datos.

## **Configuración del Entorno Python**

Para configurar el entorno de Python y poder ejecutar la herramienta, siga estos pasos:

1. Cree un entorno virtual utilizando el siguiente comando:

```bash
python3 -m venv venv

```

1. Instale las dependencias necesarias utilizando el archivo **`requirements.txt`**:

```bash
pip install -r requirements.txt

```

## **Configuración de Credenciales y Ajustes**

Siga los siguientes pasos para configurar las credenciales y ajustes de la herramienta:

1. Descargue las credenciales de Google Cloud en formato JSON desde su cuenta de Google Cloud Platform. Guarde el archivo descargado junto a este archivo README con el nombre "credentials.json".
2. Edite los datos del archivo **`config.txt`** con la siguiente información:
    - **`OPENAI`**: La API key de OpenAI.
    - **`FOLDER_ID`**: La ID de la carpeta de Google Drive donde se subirán los archivos.
    - **`EMAIL_SENDER`**: La dirección de correo electrónico desde la cual se enviarán los reportes a los vendedores.
    - **`EMAIL_PASS`**: La contraseña para aplicaciones del correo electrónico desde el cual se enviarán los reportes a los vendedores.
3. Si es necesario, puede editar el prompt utilizado para solicitar el reporte a ChatGPT, editando el archivo **`prompt.txt`**.

## **Anexo: Obtención de Contraseña para Aplicaciones de Email y Configuración del Email para Envíos Automáticos**

Para obtener la contraseña para aplicaciones del correo electrónico y configurar el email para envíos automáticos, se recomienda seguir el tutorial disponible en el siguiente enlace:

[Tutorial: Enviar Correo Electrónico vía Gmail y SMTP](https://recursospython.com/guias-y-manuales/enviar-correo-electronico-via-gmail-y-smtp/)

---

**Nota:** Asegúrese de seguir estos pasos cuidadosamente para garantizar el correcto funcionamiento de la herramienta. Si necesita ayuda adicional, no dude en ponerse en contacto con el equipo de soporte.

   
