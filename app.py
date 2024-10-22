from flask import Flask, render_template, request, session, redirect, url_for
app = Flask(__name__)
app.secret_key = "unaclavesecreta"

@app.route("/")
def index():
    if 'registros' not in session:
        session['registros'] = []
    if 'counter' not in session:
        session['counter'] = 1
    return render_template('index.html', registros=session['registros'])

@app.route("/nuevo")
def nuevo():
    return render_template('nuevo.html')

@app.route("/procesa", methods=['POST'])
def procesa():
    fecha = request.form.get('fecha')
    nombre = request.form.get('nombre')
    apellidos = request.form.get('apellidos')
    turno = request.form.get('turno')
    seminarios = request.form.getlist('seminarios')

    if 'registros' not in session:
        session['registros'] = []
    if 'counter' not in session:
        session['counter'] = 1

    session['registros'].append({
        'id': session['counter'],
        'fecha': fecha,
        'nombre': nombre,
        'apellidos': apellidos,
        'turno': turno,
        'seminarios': seminarios
    })
    
    session['counter'] += 1
    session.modified = True
    return redirect(url_for("index"))

@app.route("/editar/<int:id>")
def editar(id):
    registro = next((r for r in session['registros'] if r['id'] == id), None)
    return render_template('editar.html', registro=registro)

@app.route("/actualizar/<int:id>", methods=['POST'])
def actualizar(id):
    fecha = request.form.get('fecha')
    nombre = request.form.get('nombre')
    apellidos = request.form.get('apellidos')
    turno = request.form.get('turno')
    seminarios = request.form.getlist('seminarios')

    for i, registro in enumerate(session['registros']):
        if registro['id'] == id:
            session['registros'][i] = {
                'id': id,
                'fecha': fecha,
                'nombre': nombre,
                'apellidos': apellidos,
                'turno': turno,
                'seminarios': seminarios
            }
            break
    
    session.modified = True
    return redirect(url_for('index'))

@app.route("/eliminar/<int:id>", methods=['POST'])
def eliminar(id):
    session['registros'] = [r for r in session['registros'] if r['id'] != id]
    session.modified = True
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)