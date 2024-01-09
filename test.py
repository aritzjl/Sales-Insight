from googleapiclient.discovery import build
from google.oauth2 import service_account

def list_files(service, folder_id):
    # Obtener la lista de archivos en la carpeta
    results = service.files().list(q=f"'{folder_id}' in parents", fields="files(name, id, mimeType)").execute()
    files = results.get('files', [])

    if not files:
        print('No se encontraron archivos en la carpeta.')
    else:
        print('Archivos en la carpeta:')
        for file in files:
            if file['mimeType'] == 'application/vnd.google-apps.folder':
                print(f'Carpeta: %{file["name"]}% (ID: {file["id"]})')
                # Recursivamente listar archivos dentro de la carpeta encontrada
                list_files(service, file['id'])
            else:
                print(f'Archivo: {file["name"]} (ID: {file["id"]})')

# Credenciales y configuración
creds = service_account.Credentials.from_service_account_file('light-router-385414-9c28f10f787b.json')  # Reemplaza con tus credenciales
drive_service = build('drive', 'v3', credentials=creds)

# ID de la carpeta de Google Drive
folder_id = '1h8haP-C2Tix6C0Ri8KDQD-Hz2XR1Be3E'  # Reemplaza con el ID de tu carpeta

list_files(drive_service, folder_id)
