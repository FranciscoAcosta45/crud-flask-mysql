from flask import Flask, request
import json
import mariadb

app = Flask(__name__)
app.config["DEBUG"] = True

try:
    conn = mariadb.connect(
        user = 'root',
        password = '',
        host = '127.0.0.1',
        port = 3306,
        database = 'school'
    )
except mariadb.Error as e:
    print(print(f"Error connecting to MariaDB Platform: {e}"))

cur = conn.cursor()


@app.route('/alumno', methods=['GET'])
def index():
   cur.execute("select * from alumno")

   row_headers=[x[0] for x in cur.description]
   rv = cur.fetchall()
   json_data=[]
   for result in rv:
        json_data.append(dict(zip(row_headers,result)))

   return json.dumps(json_data)

@app.route('/add/alumno', methods=['POST'])
def addAlumno():
    matricula = request.json['Matricula']
    nombre = request.json['Nombre']
    correo = request.json['Correo']
    numeroCelular = request.json['Numero_Celular']
    edad = request.json['Edad']

    try: 
        cur.execute("INSERT INTO alumno (MATRICULA, NOMBRE, CORREO, NUMERO_CELULAR, EDAD) VALUES (?, ?, ?, ?, ?)", (matricula, nombre, correo, numeroCelular, edad))
    except mariadb.Error as e: 
        print(f"Error: {e}")

    conn.commit()
    return "recibido"

@app.route('/update/alumno', methods=['POST'])
def updateAlumno():

    matricula = request.json['Matricula']
    edad = request.json['Edad']

    try: 
        cur.execute("UPDATE alumno set EDAD=? where MATRICULA=?", (edad, matricula))
    except mariadb.Error as e: 
        print(f"Error: {e}")

    conn.commit()
    return "recibido"

@app.route('/delete/alumno', methods=['DELETE'])
def delateAlumno():

    matricula = '6243'

    try: 
        cur.execute("DELETE FROM alumno where MATRICULA='%s'" % (matricula))
    except mariadb.Error as e: 
        print(f"Error: {e}")

    conn.commit()
    return "recibido"


# run the app
app.run()