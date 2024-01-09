import os
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.discovery import build
from google.oauth2 import service_account
import sqlite3
from pydub import AudioSegment
from openai import OpenAI
client=OpenAI(api_key="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")
# Conexión a la base de datos (creará el archivo si no existe)
conn = sqlite3.connect('insights.db')
cursor = conn.cursor()

# Credenciales y configuración de la API de Google Drive
creds = service_account.Credentials.from_service_account_file('credentials.json')  # Reemplaza con tus credenciales
drive_service = build('drive', 'v3', credentials=creds)
folder_id = '1h8haP-C2Tix6C0Ri8KDQD-Hz2XR1Be3E'  # ID de la carpeta principal

# Directorio donde se guardarán los archivos descargados y convertidos
download_dir = './downloads'
os.makedirs(download_dir, exist_ok=True)  # Crea el directorio si no existe

# Obtener la lista de nombres de carpetas dentro de la carpeta principal
results = drive_service.files().list(
    q=f"'{folder_id}' in parents and mimeType='application/vnd.google-apps.folder'",
    fields="files(name, id)").execute()
folders = results.get('files', [])

if folders:
    """for folder in folders:
        folder_name = folder['name']
        folder_id = folder['id']
        
        # Listar archivos .amr y .mp3 dentro de la carpeta
        results = drive_service.files().list(
            q=f"'{folder_id}' in parents and (mimeType='audio/amr' or mimeType='audio/mp3')",
            fields="files(name, id)").execute()
        files = results.get('files', [])

        if files:
            for file in files:
                file_name = file['name']
                file_id = file['id']
                
                # Verificar si el nombre del archivo no está en la tabla de llamadas de la base de datos
                query = cursor.execute("SELECT filename FROM llamadas WHERE filename=?", (file_name,))
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
                    else:
                        print(f"Archivo '{file_name}' en la carpeta '{folder_name}' descargado.")
        else:
            print(f"No se encontraron archivos de audio en la carpeta '{folder_name}'.")"""
            
    #Ahora, vamos a procesar los .mp3 guardados con chat openAI speech to text
    # Directorio donde se encuentran los archivos
    directorio = './downloads'

    # Obtener los nombres de los archivos en el directorio
    archivos = os.listdir(directorio)

    # Filtrar para obtener solo los nombres de archivos, excluyendo directorios
    nombres_archivos = [archivo for archivo in archivos if os.path.isfile(os.path.join(directorio, archivo))]
    for archivo in nombres_archivos:
        audio_file= open("./downloads/"+archivo, "rb")
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
        archivoNombre=archivo.split(".")[0]+".txt"
        open(archivoNombre,"w").write(reporteGPT)
        
        
else:
    print("No se encontraron carpetas dentro de la carpeta principal.")
