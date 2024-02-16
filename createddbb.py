import mariadb
import sys
from connect import conectar
# Conectarse a la base de datos MariaDB
try:
    conn = conectar()
except mariadb.Error as e:
    print(f"Error de conexión a MariaDB: {e}")
    sys.exit(1)

# Obtener el cursor
cur = conn.cursor()

# Crear la tabla 'empresa' si no existe
cur.execute('''CREATE TABLE IF NOT EXISTS empresa (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(255) NOT NULL
             )''')

# Crear la tabla 'telefono' si no existe
cur.execute('''CREATE TABLE IF NOT EXISTS telefono (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(255) NOT NULL,
                numero_telefono_nombre_carpeta VARCHAR(255) NOT NULL,
                empresa_id INT,
                FOREIGN KEY (empresa_id) REFERENCES empresa(id)
             )''')

# Crear la tabla 'llamada' si no existe
cur.execute('''CREATE TABLE IF NOT EXISTS llamada (
                id INT AUTO_INCREMENT PRIMARY KEY,
                telefono_id INT,
                transcripcion TEXT,
                fecha_hora DATETIME,
                nombre_archivo VARCHAR(255),
                reporte TEXT,
                enlace_archivo VARCHAR(255),
                FOREIGN KEY (telefono_id) REFERENCES telefono(id)
             )''')

# Cerrar la conexión
conn.close()
