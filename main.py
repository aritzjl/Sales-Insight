import os
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.discovery import build
from google.oauth2 import service_account
import sqlite3
from pydub import AudioSegment
from openai import OpenAI
from datetime import datetime
from email.message import EmailMessage
import ssl
import smtplib
import time


def cargar_configuracion(archivo):
    configuracion = {}
    with open(archivo, 'r') as f:
        for linea in f:
            clave, valor = linea.strip().split('=')
            configuracion[clave] = valor
    return configuracion

# Cargar la configuración desde el archivo config.txt
configuracion = cargar_configuracion('config.txt')

# Guardar la información en variables
OPENAI = configuracion.get('OPENAI')
FOLDER_ID = configuracion.get('FOLDER_ID')
EMAIL_SENDER = configuracion.get('EMAIL_SENDER')
EMAIL_PASS = configuracion.get('EMAIL_PASS')



def enviar_reporte_via_mail(reporte,email):
    
    email_emisor = EMAIL_SENDER
    email_contra = EMAIL_PASS
    email_receptor = email
    email_subject = "Reporte sobre tu última llamada:"
    email_body = reporte

    em = EmailMessage()
    em["From"] = email_emisor
    em["To"] = email_emisor
    em["Subject"] = email_subject
    em.set_content(email_body)
    contexto = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=contexto) as mensaje:
        mensaje.login(email_emisor, email_contra)
        mensaje.sendmail(email_emisor, email_receptor, em.as_string())



def obtener_email_por_telefono(numero_telefono):
    # Conectar a la base de datos
    conn = sqlite3.connect('insights.db')
    c = conn.cursor()

    # Buscar el email asociado al número de teléfono en la tabla 'telefono'
    c.execute("SELECT email FROM telefono WHERE numero_telefono_nombre_carpeta = ?", (numero_telefono,))
    resultado = c.fetchone()

    # Cerrar la conexión y retornar el email si se encuentra, None en caso contrario
    conn.close()
    if resultado:
        return resultado[0]
    else:
        return None
    
    

def obtener_id_telefono(numero_telefono):
    # Conectar a la base de datos
    conn = sqlite3.connect('insights.db')
    c = conn.cursor()

    # Buscar el ID del número de teléfono en la tabla 'telefono'
    c.execute("SELECT id FROM telefono WHERE numero_telefono_nombre_carpeta = ?", (numero_telefono,))
    resultado = c.fetchone()

    # Cerrar la conexión y retornar el ID del teléfono si se encuentra, None en caso contrario
    conn.close()
    if resultado:
        return resultado[0]
    else:
        return None


def guardar_llamada(llamada_info):
    # Conectar a la base de datos
    conn = sqlite3.connect('insights.db')
    c = conn.cursor()

    # Obtener la fecha y hora actual
    fecha_hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Insertar los datos de la llamada en la tabla 'llamada'
    c.execute("INSERT INTO llamada (telefono_id, transcripcion, fecha_hora, nombre_archivo, reporte, enlace_archivo) VALUES (?, ?, ?, ?, ?, ?)", llamada_info)
    
    # Guardar los cambios y cerrar la conexión
    conn.commit()
    conn.close()


def revisar_archivos():
    client=OpenAI(api_key=OPENAI)
    # Conexión a la base de datos (creará el archivo si no existe)
    conn = sqlite3.connect('insights.db')
    cursor = conn.cursor()

    # Credenciales y configuración de la API de Google Drive
    creds = service_account.Credentials.from_service_account_file('credentials.json')  # Reemplaza con tus credenciales
    drive_service = build('drive', 'v3', credentials=creds)
    FOLDER_ID = '1h8haP-C2Tix6C0Ri8KDQD-Hz2XR1Be3E'  # ID de la carpeta principal

    # Directorio donde se guardarán los archivos descargados y convertidos
    download_dir = './downloads'
    os.makedirs(download_dir, exist_ok=True)  # Crea el directorio si no existe

    # Obtener la lista de nombres de carpetas dentro de la carpeta principal
    results = drive_service.files().list(
        q=f"'{FOLDER_ID}' in parents and mimeType='application/vnd.google-apps.folder'",
        fields="files(name, id)").execute()
    folders = results.get('files', [])


    if folders:
        for folder in folders:
            folder_name = folder['name']
            FOLDER_ID = folder['id']
            
            # Listar archivos .amr y .mp3 dentro de la carpeta
            results = drive_service.files().list(
                q=f"'{FOLDER_ID}' in parents and (mimeType='audio/amr' or mimeType='audio/mp3')",
                fields="files(name, id)").execute()
            files = results.get('files', [])

            if files:
                for file in files:
                    file_name = file['name']
                    file_id = file['id']
                    # Obtener la información del archivo
                    file_info = drive_service.files().get(fileId=file_id, fields='webViewLink').execute()

                    # Extraer la URL del archivo
                    file_url = file_info['webViewLink']

                    # Verificar si el nombre del archivo no está en la tabla de llamadas de la base de datos
                    query = cursor.execute("SELECT enlace_archivo FROM llamada WHERE enlace_archivo=?", (file_url,))
                    if not query.fetchone():
                        file_path = os.path.join(download_dir, file_name)
                        
                        # Descargar el archivo en el directorio de descargas
                        request = drive_service.files().get_media(fileId=file_id)
                        with open(file_path, 'wb') as f:
                            downloader = MediaIoBaseDownload(f, request)
                            done = False
                            while not done:
                                status, done = downloader.next_chunk()
                        
                        # Convertir .amr a .mp3
                        if file_name.endswith('.amr'):
                            sound = AudioSegment.from_file(file_path, format="amr")
                            mp3_file_name = os.path.splitext(file_name)[0] + '.mp3'
                            mp3_file_path = os.path.join(download_dir, mp3_file_name)
                            sound.export(mp3_file_path, format="mp3")
                            os.remove(file_path)  # Eliminar el archivo .amr original
                            print(f"Archivo '{file_name}' convertido y guardado como '{mp3_file_name}' en la carpeta '{folder_name}'.")
                            file_name=mp3_file_name
                        else:
                            print(f"Archivo '{file_name}' en la carpeta '{folder_name}' descargado.")
                            
                        id_telefono = obtener_id_telefono(folder_name)
                        
                        
                        
                        audio_file= open("./downloads/"+file_name, "rb")
                        
                        
                        transcript = client.audio.transcriptions.create(
                        model="whisper-1", 
                        file=audio_file, 
                        response_format="text"
                        )  

                        
                        messages=[]
                        
                        mensaje=open('prompt.txt','r').read()
                        message={"role": "assistant", "content": mensaje}
                        messages.append(message)
                        
                        message={"role": "user", "content": transcript}
                        messages.append(message)
                        
                        completion = client.chat.completions.create(
                        model="gpt-3.5-turbo-16k",
                        messages=messages
                        )

                        reporteGPT=completion.choices[0].message.content
                        archivoNombre=file_name.split(".")[0]+".txt"
                        open(archivoNombre,"w").write(reporteGPT)      
                    
                        fecha_hora_texto = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        llamada_info=[id_telefono,transcript,fecha_hora_texto,file_name,reporteGPT,file_url]
                        
                        guardar_llamada(llamada_info)
                        email=obtener_email_por_telefono(folder_name)
                        enviar_reporte_via_mail(reporteGPT,email)
                
while True:
    revisar_archivos()
    time.sleep(5)
