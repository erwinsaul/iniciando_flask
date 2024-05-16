from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'flask'

conexion = MySQL(app)

@app.before_request
def before_request():
    print('Antes de la petición')

@app.after_request
def after_request(response):
    print('Despues de la petición')
    return response

@app.route('/')

def index():
    #return '<h1>Mensaje</h1>'
    cursos =['PHP','Python','Java', 'C++', 'JavaScript', 'C#']
    data = {
        'titulo': 'ESC_APP',
        'bienvenida': 'Bienvenido al curso de Flask',
        'cursos': cursos,
        'numero_cursos': len(cursos)
    }
    return render_template('index.html', data=data)

@app.route('/contacto/<nombre>')
def contacto(nombre):
    data = {
        'titulo': 'Contacto',
        'nombre': nombre
    }
    return render_template('contacto.html', data=data)

@app.route('/contacto/<nombre>/<int:edad>')
def contacto2(nombre, edad):
    data = {
        'titulo': 'Contacto',
        'nombre': nombre,
        'edad':edad
    }
    return render_template('contacto.html', data=data)

def query_string():
    print(request)
    print(request.args)
    print(request.args.get('p'))
    print(request.args.get('p1'))
    print(request.args.get('p2'))
    return("OK")

@app.route('/cursos')
def cursos():
    data ={}
    try:
        cursor = conexion.connection.cursor()
        sql ='select * from cursos ORDER BY nombre ASC'
        cursor.execute(sql)
        res = cursor.fetchall()        
        data['cursos'] = res
        data['mensaje'] = 'OK'
    except Exception as e:
        data['mensaje'] = str(e)
    return jsonify(data)

def pagina_no_encontrada(error):
    data = {
        'titulo': 'Página no encontrada',
        'error': str(error)
    }
    return render_template('404.html', data= data), 404

if __name__ == '__main__':  
    app.add_url_rule('/query', view_func=query_string)
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True, host='0.0.0.0', port=5000)
