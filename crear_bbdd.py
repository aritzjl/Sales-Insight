import sqlite3

# Conectarse a la base de datos (si no existe, se creará)
conn = sqlite3.connect('insights.db')
c = conn.cursor()

# Crear la tabla 'empresa'
c.execute('''CREATE TABLE IF NOT EXISTS empresa (
                id INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL
             )''')

# Crear la tabla 'telefono'
c.execute('''CREATE TABLE IF NOT EXISTS telefono (
                id INTEGER PRIMARY KEY,
                email TEXT NOT NULL,
                numero_telefono_nombre_carpeta TEXT NOT NULL,
                empresa_id INTEGER,
                FOREIGN KEY (empresa_id) REFERENCES empresa(id)
             )''')

# Crear la tabla 'llamada'
c.execute('''CREATE TABLE IF NOT EXISTS llamada (
                id INTEGER PRIMARY KEY,
                telefono_id INTEGER,
                transcripcion TEXT,
                fecha_hora TEXT,
                nombre_archivo TEXT,
                reporte TEXT,
                enlace_archivo TEXT,
                FOREIGN KEY (telefono_id) REFERENCES telefono(id)
             )''')

# Guardar los cambios y cerrar la conexión
conn.commit()
conn.close()
