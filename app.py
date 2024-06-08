from flask import Flask, redirect, url_for, render_template, request
from pymongo import MongoClient
from bson import ObjectId
from werkzeug.utils import secure_filename
from datetime import datetime
import os

# sudah dipindahkan ke file .env
client = MongoClient('mongodb+srv://test:sparta@cluster0.6vz5zah.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client.fgd2

# dotenv_path = join(dirname(__file__), '.env')
# load_dotenv(dotenv_path)

# MONGODB_URI = os.environ.get("MONGODB_URI")
# DB_NAME =  os.environ.get("DB_NAME")

# client = MongoClient(MONGODB_URI)
# db = client[DB_NAME]

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def home():
    fruit = list(db.fruit.find({}))
    return render_template('dashboard.html', fruit = fruit)

@app.route('/fruit', methods = ['GET', 'POST'])
def fruit():
    fruit = list(db.fruit.find({}))
    return render_template('fruit.html', fruit = fruit)

@app.route('/AddFruit', methods = ['GET', 'POST'])
def AddFruit():
    if request.method == 'POST':
        nama = request.form['nama']
        harga = request.form['harga']
        gambar = request.files['gambar']
        deskripsi = request.form['deskripsi']

        extension = gambar.filename.split('.')[-1]
        today = datetime.now()
        mytime = today.strftime('%Y-%m-%d %H-%M-%S')
        gambar_name = f'gambar-{mytime}.{extension}'
        save_to = f'static/assets/ImgFruit/{gambar_name}'
        gambar.save(save_to)

        doc = {
            'nama' : nama,
            'harga' : harga,
            'gambar' : gambar_name,
            'deskripsi' : deskripsi
        }
        db.fruit.insert_one(doc)
        # Handle POST Request here
        return redirect(url_for('fruit'))
    return render_template('AddFruit.html')

@app.route('/EditFruit/<_id>', methods = ['GET', 'POST'])
def EditFruit(_id):
    if request.method == 'POST':
        nama = request.form['nama']
        harga = request.form['harga']
        gambar = request.files['gambar']
        deskripsi = request.form['deskripsi']

        extension = gambar.filename.split('.')[-1]
        today = datetime.now()
        mytime = today.strftime('%Y-%M-%d-%H-%m-%S')
        gambar_name = f'gambar-{mytime}.{extension}'
        save_to = f'static/assets/ImgFruit/{gambar_name}'
        gambar.save(save_to)

        doc = {
            'nama' : nama,
            'harga' : harga,
            'deskripsi' : deskripsi
        }
        if gambar:
            doc['gambar'] = gambar_name
        db.fruit.update_one({'_id' : ObjectId(_id)}, {'$set' : doc})
        # Handle POST Request here
        return redirect(url_for('fruit'))
    id = ObjectId(_id)
    data = list(db.fruit.find({'_id' : id}))
    return render_template('EditFruit.html', data = data)

@app.route('/DeleteFruit/<_id>', methods = ['GET', 'POST'])
def DeleteFruit(_id):
    id = ObjectId(_id)
    db.fruit.delete_one({'_id' : id})
    return redirect(url_for('fruit'))

if __name__ == '__main__':
    # DEBUG is SET to TRUE, CHANGE FOR PROD
    app.run('0.0.0.0', port = 5000, debug = True)