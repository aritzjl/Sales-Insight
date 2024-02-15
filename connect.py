import mariadb
def conectar():    
    conn = mariadb.connect(
        user="",
        password="",
        host="",  # Suponiendo que la base de datos está en el mismo servidor
        port="",  # El puerto predeterminado para MariaDB
        database="GPTSales"  # Reemplaza esto con el nombre de tu base de datos
    )
    return conn