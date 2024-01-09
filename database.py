import sqlite3

# Conexión a la base de datos (creará el archivo si no existe)
conn = sqlite3.connect('insights.db')
cursor = conn.cursor()

# Crear tabla empresas con ID automático
cursor.execute('''CREATE TABLE empresas (
                    empresaid INTEGER PRIMARY KEY,
                    empresanombre TEXT
                )''')

# Crear tabla empleado con ID automático
cursor.execute('''CREATE TABLE empleado (
                    empleado_id INTEGER PRIMARY KEY,
                    nombre TEXT,
                    apellido TEXT,
                    email TEXT,
                    numtlf TEXT,
                    empresaid INTEGER,
                    FOREIGN KEY(empresaid) REFERENCES empresas(empresaid)
                )''')

# Crear tabla llamadas con ID automático
cursor.execute('''CREATE TABLE llamadas (
                    llamada_id INTEGER PRIMARY KEY,
                    empleadoid INTEGER,
                    filename TEXT,
                    fecha DATE,
                    FOREIGN KEY(empleadoid) REFERENCES empleado(empleado_id)
                )''')


# Insertar una empresa manualmente
cursor.execute("INSERT INTO empresas (empresanombre) VALUES ('Empresa ABC')")
empresa_id = cursor.lastrowid  # ID de la empresa recién insertada

# Insertar dos empleados asociados a la empresa manualmente
empleados = [
    ("Juan", "García", "juan@example.com", "56990009199", empresa_id),
    ("María", "López", "maria@example.com", "56992310135", empresa_id)
]

for empleado in empleados:
    cursor.execute("INSERT INTO empleado (nombre, apellido, email, numtlf, empresaid) VALUES (?, ?, ?, ?, ?)",
                   empleado)


# Guardar los cambios y cerrar la conexión
conn.commit()
conn.close()

print("Base de datos 'insights.db' creada con las tablas empresas, empleado y llamadas con IDs generados automáticamente.")
