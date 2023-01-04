from flask import Flask, render_template, url_for, request, redirect, flash
import requests, json

application = Flask(__name__)
application.secret_key = "teuayanunyahoisina"

@application.route('/')
def index():
    return render_template('index.html')

@application.route('/driverRead')  
def driverRead():

    response = requests.get("http://localhost:8000/api/driver")        # request data dari API
    if response.status_code == 200: flash('Berhasil menambahkan data!')     # feedback ke user
    else: flash('Gagal menambahkan data!')

    return render_template('driverRead.html', data=response.json()['results'])


@application.route('/driverInsert', methods=['GET', 'POST']) 
def driverInsert():				

    if request.method =='GET':
        return render_template('driverInsert.html')

    if request.method =='POST':
        nama = request.form['nama']					                    # request form yang ada di html
        username = request.form['username']				
        password = request.form['password']

        url = "http://localhost:8000/api/driver/create"                    # route API untuk create

        data_json=json.dumps({"nama": nama,                     # ubah data jadi format JSON ({"key" : "value"}, {"key" : "value"}, ...)
                              "username": username,                                 # "key"   = harus sama dengan yang ada di FastAPI > App > schema.py
                              "password": password                           # "value" = dari request form HTML
                            })

        print("data JSON\n",data_json)                                      # cek datanya, udah jadi JSON belum
        response = requests.post(url, data=data_json)                       # request POST ke API dengan data hasil input form yang udah diubah ke JSON

        if response.status_code == 200: flash('Berhasil menambahkan data!') # feedback ke user
        else: flash('Gagal menambahkan data!')

        return redirect(url_for('driverRead'))	


@application.route('/driverEdit/<int:id>', methods=['GET', 'POST'])
def driverEdit(id):
    if request.method =='GET':
        response = requests.get("http://localhost:8000/api/driver"+str(id))           # request data yang lama dari API
        return render_template('driverEdit.html', data=response.json()['results'])

    if request.method == 'POST':
        nama = request.form['nama']					                    # request form yang ada di html
        username = request.form['username']				
        password = request.form['password']

        url = "http://localhost:8000/api/driver/update"                    # route API untuk create

        data_json=json.dumps({"nama": nama,                     # ubah data jadi format JSON ({"key" : "value"}, {"key" : "value"}, ...)
                              "username": username,                                 # "key"   = harus sama dengan yang ada di FastAPI > App > schema.py
                              "password": password                           # "value" = dari request form HTML
                            })

        print("data JSON\n",data_json)                                                  # cek datanya, udah jadi JSON belum
        response = requests.put(url, data=data_json)                                    # request PUT ke API dengan data hasil input form yang udah diubah ke JSON

        if response.status_code == 200: flash('Berhasil mengupdate data!')              # feedback ke user
        else: flash('Gagal mengupdate data!')
        
        return redirect(url_for('driver'))


@application.route('/driverDelete/<int:id>')
def driverDelete(id):

    url = "http://localhost:8000/api/driver/delete" + str(id)         # route API untuk delete + id terpilih

    response = requests.delete(url)                                     # request DELETE ke API dengan id terpilih
    
    if response.status_code == 200: flash('Berhasil menghapus data!')   # feedback ke user
    else: flash('Gagal menghapus data!')

    return redirect(url_for('driver'))

@application.route('/bipolRead')  
def bipolRead():

    response = requests.get("http://localhost:8000/api/bipol")        # request data dari API
    if response.status_code == 200: flash('Berhasil menambahkan data!')     # feedback ke user
    else: flash('Gagal menambahkan data!')

    return render_template('bipolRead.html', data=response.json()['results'])


@application.route('/bipolInsert', methods=['GET', 'POST']) 
def bipolInsert():				

    if request.method =='GET':
        return render_template('bipolInsert.html')

    if request.method =='POST':
        id = request.form['id']					                    # request form yang ada di html
        platnomor = request.form['platnomor']				
        driver = request.form['driver']

        url = "http://localhost:8000/api/bipol/create"                    # route API untuk create

        data_json=json.dumps({"id_bipol": id,                     # ubah data jadi format JSON ({"key" : "value"}, {"key" : "value"}, ...)
                              "plat_nomor": platnomor,                                 # "key"   = harus sama dengan yang ada di FastAPI > App > schema.py
                              "id_driver": driver                           # "value" = dari request form HTML
                            })

        print("data JSON\n",data_json)                                      # cek datanya, udah jadi JSON belum
        response = requests.post(url, data=data_json)                       # request POST ke API dengan data hasil input form yang udah diubah ke JSON

        if response.status_code == 200: flash('Berhasil menambahkan data!') # feedback ke user
        else: flash('Gagal menambahkan data!')

        return redirect(url_for('bipolRead'))	


@application.route('/bipolEdit/<int:id>', methods=['GET', 'POST'])
def bipolEdit(id):
    if request.method =='GET':
        response = requests.get("http://localhost:8000/api/bipol"+str(id))           # request data yang lama dari API
        return render_template('bipolEdit.html', data=response.json()['results'])

    if request.method == 'POST':
        id = request.form['id']					                    # request form yang ada di html
        platnomor = request.form['platnomor']				
        driver = request.form['driver']

        url = "http://localhost:8000/api/bipol/update" + str(id)                     # route API untuk update + id terpilih

        data_json=json.dumps({"id_bipol": id,                     # ubah data jadi format JSON ({"key" : "value"}, {"key" : "value"}, ...)
                            "plat_nomor": platnomor,                                 # "key"   = harus sama dengan yang ada di FastAPI > App > schema.py
                            "id_driver": driver                           # "value" = dari request form HTML
                        })

        print("data JSON\n",data_json)                                                  # cek datanya, udah jadi JSON belum
        response = requests.put(url, data=data_json)                                    # request PUT ke API dengan data hasil input form yang udah diubah ke JSON

        if response.status_code == 200: flash('Berhasil mengupdate data!')              # feedback ke user
        else: flash('Gagal mengupdate data!')
        
        return redirect(url_for('bipol'))


@application.route('/bipolDelete/<int:id>')
def bipolDelete(id):

    url = "http://localhost:8000/api/bipol/delete" + str(id)         # route API untuk delete + id terpilih

    response = requests.delete(url)                                     # request DELETE ke API dengan id terpilih
    
    if response.status_code == 200: flash('Berhasil menghapus data!')   # feedback ke user
    else: flash('Gagal menghapus data!')

    return redirect(url_for('bipol'))

@application.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# @application.route('/dashboardDriver')
# def dashboardDriver():
#     return render_template('dashboardDriver.html')

if __name__ == '__main__':
    application.run(debug=True)