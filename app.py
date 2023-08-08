from flask import Flask, render_template, request, redirect, url_for, jsonify
import json

app = Flask(__name__)

def cargar_datos():
    with open('data/datos.json', 'r') as archivo:
        datos = json.load(archivo)
    return datos

def guardar_datos(datos):
    with open('data/datos.json', 'w') as archivo:
        json.dump(datos, archivo, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']

        datos = cargar_datos()

        for cuenta in datos['cuentas']:
            if cuenta['usuario'] == usuario and cuenta['contrasena'] == contrasena:
                return redirect(url_for('simulacion', usuario=usuario))
        
        return render_template('login.html', mensaje='Credenciales incorrectas')

    return render_template('login.html')

@app.route('/simulacion/<usuario>', methods=['GET', 'POST'])
def simulacion(usuario):
    datos = cargar_datos()

    accion = 'transferir'

    if request.method == 'POST':
        accion = request.form['accion']

        for cuenta in datos['cuentas']:
            if cuenta['usuario'] == usuario:
                if accion == 'ingresar':
                    monto = float(request.form['monto'])
                    cuenta['saldo'] += monto
                elif accion == 'transferir':
                    destinatario = request.form['destinatario']
                    monto = float(request.form['monto'])
                    for otra_cuenta in datos['cuentas']:
                        if otra_cuenta['usuario'] == destinatario:
                            cuenta['saldo'] -= monto
                            otra_cuenta['saldo'] += monto
                elif accion == 'pedir':
                    destinatario = request.form['destinatario']
                    monto = float(request.form['monto'])
                    for otra_cuenta in datos['cuentas']:
                        if otra_cuenta['usuario'] == destinatario:
                            cuenta['saldo'] += monto
                            otra_cuenta['saldo'] -= monto

                guardar_datos(datos)

    for cuenta in datos['cuentas']:
        if cuenta['usuario'] == usuario:
            saldo_actual = cuenta['saldo']
            break

    return render_template('simulacion.html', usuario=usuario, saldo_actual=saldo_actual, accion=accion) 

if __name__ == '__main__':
    app.run(debug=True)
