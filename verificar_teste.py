from django.db import connection

# ... dentro de uma função do modelo Usuario ou view
with connection.cursor() as cursor:
    cursor.execute("SELECT * FROM beaba_schema.usuario;")  # Consulta com o esquema
    print(cursor.query)
