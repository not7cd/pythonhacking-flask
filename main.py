import time
from flask import Flask, render_template, jsonify, request
from database import db_session, init_db
from models.car import Car

app = Flask(__name__)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return render_template('index.html', name=request.form['name'])
    else:
        return render_template('index.html')


@app.route('/some_json')
def some_json():
    dict_ = {
        'hs': 3,
        'timestamp': time.time(),
    }
    return jsonify(dict_)
 

@app.route('/hs/<int:number>')
def hackerspace(number):
    l = [x**3 for x in range(1, number+1)]
    return str(l)


@app.route('/form', methods=['GET', 'POST'])
def formularz():
    if request.method == 'POST':
        return render_template('site.html', name=request.form['name'])
    if request.method == 'GET':
        return render_template('form.html')


@app.route('/szablon')
def szablony():
    lista_zakupow = ['mleko', 'jajka']
    return render_template('szablon.html', haha={'costam': 'hahaha, jednak nie'}, zakupy=lista_zakupow)


@app.route('/list_cars')
def car_club():
    cars = Car.query.all()
    return render_template('car_club.html', auta=cars)


@app.route('/add_car', methods=['POST'])
def add_car():
    data = request.json
    c = Car(id=data['id'], make=data['make'],
            model=data['model'], plates=data['plates'],
            dmv_number=data['dmv'], year=data['year'])
    db_session.add(c)
    db_session.commit()
    return 'Success\n'


@app.route('/car_form')
def car_form():
    if request.method == 'POST':
        return render_template('car_club.html', name=request.form['name'])
    if request.method == 'GET':
        return render_template('form.html')


if __name__ == '__main__':
    init_db()
    app.run()
