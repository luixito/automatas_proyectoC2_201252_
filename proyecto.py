from flask import Flask, render_template, request, redirect, url_for, session
import csv
import re

app = Flask(__name__)
app.secret_key = 'clave_secreta'  # Cambia esto con una clave segura en un entorno de producción

def validar_password(password):
    regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,15}$"
    return re.match(regex, password) is not None

def cargar_registros():
    registros = []
    with open('./dataset.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            registros.append(row)
    return registros

def filtrar_registros(campo, valor, registros):
    resultados = []
    for registro in registros:
        if valor.lower() in registro[campo].lower():
            resultados.append(registro)
    return resultados

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']

        # Validar usuario y contraseña (puedes mejorar esto según tus necesidades)
        if usuario == 'tu_usuario' and validar_password(password):
            session['usuario'] = usuario
            return redirect(url_for('filtro'))
        else:
            return "Credenciales incorrectas."

    return render_template('login.html')

# Ruta principal para el filtro
@app.route('/filtro', methods=['GET', 'POST'])
def filtro():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    registros = cargar_registros()

    if request.method == 'POST':
        campo = request.form['campo']
        valor = request.form['valor']

        resultados = filtrar_registros(campo, valor, registros)

        if campo == 'Nombre Contacto':
            resultados = sorted(resultados, key=lambda x: x[campo])
        elif campo == 'Correo':
            resultados = sorted(resultados, key=lambda x: x[campo])
        elif campo == 'Clave cliente':
            resultados = sorted(resultados, key=lambda x: int(x[campo]))
            
        return render_template('response.html', resultados=resultados)

    return render_template('filtro.html')

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
