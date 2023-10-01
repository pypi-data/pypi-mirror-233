#import sqlite3
import random
import string
import mysql.connector

def generar_cadena_aleatoria(longitud):
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for _ in range(longitud))

def short(enlace_largo):
    conn = mysql.connector.connect(host="mysql-apiserver.alwaysdata.net",user="apiserver_user",password="R@ydel2022*",database="apiserver_db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS enlaces
        (id INT AUTO_INCREMENT PRIMARY KEY,
        enlace_largo VARCHAR(4294967295) NOT NULL,
        enlace_corto VARCHAR(4294967295) NOT NULL UNIQUE)''')
    c.execute("SELECT enlace_corto FROM enlaces WHERE enlace_largo=%s", (enlace_largo,))
    resultado = c.fetchone()
    if resultado is not None:
        return resultado[0]
    else:
        while True:
            enlace_corto = generar_cadena_aleatoria(6)
            try:
                c.execute("INSERT INTO enlaces (enlace_largo, enlace_corto) VALUES (%s, %s)", (enlace_largo, enlace_corto))
                conn.commit()
                conn.close()
                return enlace_corto
            except mysql.connector.IntegrityError:
                continue
    conn.close()

def unshort(enlace_corto):
    conn = mysql.connector.connect(host="mysql-apiserver.alwaysdata.net",user="apiserver_user",password="R@ydel2022*",database="apiserver_db")
    c = conn.cursor()
    c.execute("SELECT enlace_largo FROM enlaces WHERE enlace_corto=%s", (enlace_corto,))
    resultado = c.fetchone()
    conn.close()
    if resultado is not None:
        return resultado[0]
    else:
        return None