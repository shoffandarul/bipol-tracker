from flask import Flask, render_template, url_for, request, redirect, flash
from datetime import date, datetime
import requests, json, hashlib

application = Flask(__name__)
application.secret_key = "teuayanunyahoisina"

today = date.today()
def get_day():
    intDay = today.weekday()
    day = ''
    intDay = 0
    if intDay == 0: day = 'Senin'
    elif intDay == 1: day = 'Selasa'
    elif intDay == 2: day = 'Rabu'
    elif intDay == 3: day = 'Kamis'
    elif intDay == 4: day = 'Jumat'
    elif intDay == 5: day = 'Sabtu'
    elif intDay == 6: day = 'Minggu'
    return day

def format_time(waktu):
    if waktu[1] == ':' : return '0' + waktu[0] + ':' + waktu[2] + waktu[3]
    else: return waktu[0] + waktu[1] + ':' + waktu[3] + waktu[4]

@application.route('/')
@application.route('/posisi')
def index():
    # send get request
    all_data_posisi_str = (requests.get('http://localhost:8000/api/posisi/')).text # ambil data dari api
    all_data_posisi = json.loads(all_data_posisi_str)["results"]
    # send get request
    all_data_bipol_str = (requests.get('http://localhost:8000/api/bipol/')).text # ambil data dari api
    all_data_bipol = json.loads(all_data_bipol_str)["results"]
    # add plat nomor
    for i in all_data_posisi:
        for j in all_data_bipol:
            if i["id_bipol"] == j["id_bipol"]:
                data = {'plat_nomor':j["plat_nomor"]}
                i.update(data)
    print(all_data_posisi)
    # display posisi page for user
    return render_template('indexPosisi.html', data_posisi=all_data_posisi)

@application.route('/jadwal')
def jadwal():
    # send get request
    all_data_jadwal_str = (requests.get('http://localhost:8000/api/jadwal/')).text # ambil data dari api
    all_data_jadwal = json.loads(all_data_jadwal_str)["results"]
    # send get request
    all_data_bipol_str = (requests.get('http://localhost:8000/api/bipol/')).text # ambil data dari api
    all_data_bipol = json.loads(all_data_bipol_str)["results"]
    # fix format time
    for i in all_data_jadwal:
        i["waktu"] = format_time(i["waktu"])
    # get data jadwal for today
    # data_jadwal = []
    # for i in all_data_jadwal:
    #     try:
    #         if i["hari"] == 'Senin': data_jadwal.append(i)
    #     except:
    #         break
    # fix format time
    for i in all_data_jadwal:
        i["waktu"] = format_time(i["waktu"])
    # get format for sort data by time
    strTime = []
    for i in all_data_jadwal:
        strTime.append(i["waktu"])
        strTime.sort()
    strTime = dict.fromkeys(strTime)
    # get data by time
    data_jadwal = []
    for item in strTime:
        for i in all_data_jadwal:
            if i["waktu"] == item:
                data_jadwal.append(i)
    # add plat nomor
    for i in data_jadwal:
        for j in all_data_bipol:
            if i["id_bipol"] == j["id_bipol"]:
                data = {'plat_nomor':j["plat_nomor"]}
                i.update(data)
    # display jadwal page for user
    return render_template('index.html', data_jadwal=data_jadwal)

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

        url = "http://localhost:8000/api/driver/create/"                    # route API untuk create

        data_json=json.dumps({"id_driver": 0,
                              "nama": nama,                     # ubah data jadi format JSON ({"key" : "value"}, {"key" : "value"}, ...)
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
        response = requests.get("http://localhost:8000/api/driver/"+str(id))           # request data yang lama dari API
        return render_template('driverEdit.html', data=response.json()['results'])

    if request.method == 'POST':
        nama = request.form['nama']					                    # request form yang ada di html
        username = request.form['username']				
        password = request.form['password']

        url = "http://localhost:8000/api/driver/update/"+str(id)                    # route API untuk create

        data_json=json.dumps({"id_driver": id,
                              "nama": nama,                     # ubah data jadi format JSON ({"key" : "value"}, {"key" : "value"}, ...)
                              "username": username,                                 # "key"   = harus sama dengan yang ada di FastAPI > App > schema.py
                              "password": password                           # "value" = dari request form HTML
                            })

        print("data JSON\n",data_json)                                                  # cek datanya, udah jadi JSON belum
        response = requests.put(url, data=data_json)                                    # request PUT ke API dengan data hasil input form yang udah diubah ke JSON

        if response.status_code == 200: flash('Berhasil mengupdate data!')              # feedback ke user
        else: flash('Gagal mengupdate data!')
        
        return redirect(url_for('driverRead'))


@application.route('/driverDelete/<int:id>')
def driverDelete(id):

    url = "http://localhost:8000/api/driver/delete/" + str(id)         # route API untuk delete + id terpilih

    response = requests.delete(url)                                     # request DELETE ke API dengan id terpilih
    
    if response.status_code == 200: flash('Berhasil menghapus data!')   # feedback ke user
    else: flash('Gagal menghapus data!')

    return redirect(url_for('driverRead'))

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
        response = requests.get("http://localhost:8000/api/bipol/"+str(id))           # request data yang lama dari API
        
        return render_template('bipolEdit.html', data=response.json()['results'])

    if request.method == 'POST':
        id = request.form['id']					                    # request form yang ada di html
        platnomor = request.form['platnomor']				
        driver = request.form['driver']

        url = "http://localhost:8000/api/bipol/update/" + str(id)                     # route API untuk update + id terpilih

        data_json=json.dumps({"id_bipol": id,                     # ubah data jadi format JSON ({"key" : "value"}, {"key" : "value"}, ...)
                            "plat_nomor": platnomor,                                 # "key"   = harus sama dengan yang ada di FastAPI > App > schema.py
                            "id_driver": driver                           # "value" = dari request form HTML
                        })

        print("data JSON\n",data_json)                                                  # cek datanya, udah jadi JSON belum
        response = requests.put(url, data=data_json)                                    # request PUT ke API dengan data hasil input form yang udah diubah ke JSON

        if response.status_code == 200: flash('Berhasil mengupdate data!')              # feedback ke user
        else: flash('Gagal mengupdate data!')
        
        return redirect(url_for('bipolRead'))


@application.route('/bipolDelete/<int:id>')
def bipolDelete(id):

    url = "http://localhost:8000/api/bipol/delete/" + str(id)         # route API untuk delete + id terpilih

    response = requests.delete(url)                                     # request DELETE ke API dengan id terpilih
    
    if response.status_code == 200: flash('Berhasil menghapus data!')   # feedback ke user
    else: flash('Gagal menghapus data!')

    return redirect(url_for('bipolRead'))

# Eza Musyarof

@application.route('/jadwalRead')
def jadwalRead():
    # send get request
    all_data_jadwal_str = (requests.get('http://localhost:8000/api/jadwal/')).text # ambil data dari api
    all_data_jadwal = json.loads(all_data_jadwal_str)["results"]
    # send get request
    all_data_bipol_str = (requests.get('http://localhost:8000/api/bipol/')).text # ambil data dari api
    all_data_bipol = json.loads(all_data_bipol_str)["results"]
    # fix format time
    for i in all_data_jadwal:
        i["waktu"] = format_time(i["waktu"])
    # add plat nomor
    for i in all_data_jadwal:
        for j in all_data_bipol:
            if i["id_bipol"] == j["id_bipol"]:
                data = {'plat_nomor':j["plat_nomor"]}
                i.update(data)
    # display jadwalRead page
    return render_template('jadwalRead.html', data_jadwal=all_data_jadwal)

@application.route('/jadwalInsert', methods=['GET', 'POST'])
def jadwalInsert():
    # send get request
    all_data_jadwal_str = (requests.get('http://localhost:8000/api/jadwal/')).text # ambil data dari api
    all_data_jadwal = json.loads(all_data_jadwal_str)["results"]
    # send get request
    all_data_bipol_str = (requests.get('http://localhost:8000/api/bipol/')).text # ambil data dari api
    all_data_bipol = json.loads(all_data_bipol_str)["results"]
    if request.method == 'GET':
        # display jadwalInsert page
        return render_template('jadwalInsert.html', data_bipol=all_data_bipol)
    else :
        # get value
        bipol = request.form['bipol']
        # hari = request.form['hari']
        halte = request.form['halte']
        waktu = request.form['waktu']
        # get new id_jadwal
        for i in all_data_jadwal:
            id_jadwal = i["id_jadwal"] + 1
        # send post request jadwal
        url = "http://localhost:8000/api/jadwal/create"
        payload = json.dumps ({
            "id_jadwal": id_jadwal,
            "id_bipol": bipol,
            "hari": "Senin",
            "waktu": waktu,
            "halte": halte
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
        # display jadwalInsert page
        return redirect('../jadwalRead')

@application.route('/jadwalEdit/<int:id>', methods=['GET', 'POST'])
def jadwalEdit(id):
    # send get request
    data_selected_str = (requests.get('http://localhost:8000/api/jadwal/'+str(id))).text
    data_selected = json.loads(data_selected_str)["results"][0]
    # send get request
    all_data_bipol_str = (requests.get('http://localhost:8000/api/bipol/')).text # ambil data dari api
    all_data_bipol = json.loads(all_data_bipol_str)["results"]
    if request.method == 'GET':
        # convert pad 6 (00:00:00) to 4 (00:00)
        waktu = data_selected["waktu"]
        if waktu[1] == ':': waktu = '0' + waktu[0] + ':' + waktu[2] + waktu[3]
        else: waktu = waktu[0] + waktu[1] + ':' + waktu[3] + waktu[4]
        data_selected["waktu"] = waktu
        print(data_selected)
        # get plat nomor
        for i in all_data_bipol:
            if i["id_bipol"] == data_selected["id_bipol"]:
                data = {'plat_nomor':i["plat_nomor"]}
                data_selected.update(data)
        # display jadwalEdit page
        return render_template('jadwalEdit.html', data_selected=data_selected, data_bipol=all_data_bipol)
    elif request.method == 'POST':
        # get value
        id_bipol = request.form['bipol']
        halte = request.form['halte']
        # hari = request.form['hari']
        waktu = request.form['waktu']
        # send put request jadwal
        url = "http://localhost:8000/api/jadwal/update/" + str(id)
        payload = json.dumps ({
            "id_jadwal": id,
            "id_bipol": id_bipol,
            "hari": "Senin",
            "waktu": waktu+':00',
            "halte": halte
        })
        headers = { 'Content-Type': 'application/json' }
        response = requests.request("PUT", url, headers=headers, data=payload)
        print(response.text)
        # display jadwalEdit page
        return redirect('../jadwalRead')

@application.route('/jadwalDelete/<int:id>')
def jadwalDelete(id):
    # send delete request
    url = 'http://localhost:8000/api/jadwal/delete/' + str(id)
    response = requests.request("DELETE", url)
    print(response.text)
    # display jadwal 
    return redirect('../jadwalRead')

@application.route('/posisiRead')
def posisiRead():
    # send get request
    all_data_posisi_str = (requests.get('http://localhost:8000/api/posisi/')).text # ambil data dari api
    all_data_posisi = json.loads(all_data_posisi_str)["results"]
    # send get request
    all_data_bipol_str = (requests.get('http://localhost:8000/api/bipol/')).text # ambil data dari api
    all_data_bipol = json.loads(all_data_bipol_str)["results"]
    # fix format time
    for i in all_data_posisi:
        i["waktu"] = format_time(i["waktu"])
    # add plat nomor
    for i in all_data_posisi:
        for j in all_data_bipol:
            if i["id_bipol"] == j["id_bipol"]:
                data = {'plat_nomor':j["plat_nomor"]}
                i.update(data)
    # display posisiRead page
    return render_template('posisiRead.html', data_posisi=all_data_posisi)

@application.route('/posisiInsert', methods=['GET', 'POST'])
def posisiInsert():
    # send get request
    all_data_bipol_str = (requests.get('http://localhost:8000/api/bipol/')).text # ambil data dari api
    all_data_bipol = json.loads(all_data_bipol_str)["results"]
    if request.method == 'GET':
        # display posisiInsert page
        return render_template('posisiInsert.html', data_bipol=all_data_bipol)
    else :
        # get value
        bipol = request.form['bipol']
        posisi = request.form['posisi']
        kapasitas = request.form['kapasitas']
        current_datetime = datetime.now()
        waktu = str(current_datetime.strftime("%H:%M")) + ':00'
        # send post request jadwal
        url = "http://localhost:8000/api/posisi/create"
        payload = json.dumps ({
            "id_bipol": bipol,
            "posisi": posisi,
            "waktu": waktu,
            "kapasitas": kapasitas
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
        # display jadwalInsert page
        return redirect('../posisiRead')

@application.route('/posisiEdit/<int:id>', methods=['GET', 'POST'])
def posisiEdit(id):
    # send get request
    data_selected_str = (requests.get('http://localhost:8000/api/posisi/'+str(id))).text
    data_selected = json.loads(data_selected_str)["results"][0]
    # send get request
    all_data_bipol_str = (requests.get('http://localhost:8000/api/bipol/')).text # ambil data dari api
    all_data_bipol = json.loads(all_data_bipol_str)["results"]
    if request.method == 'GET':
        # get plat nomor
        for i in all_data_bipol:
            if i["id_bipol"] == data_selected["id_bipol"]:
                data = {'plat_nomor':i["plat_nomor"]}
                data_selected.update(data)
        # display posisiEdit page
        return render_template('posisiEdit.html',data_selected=data_selected, data_bipol=all_data_bipol)
    elif request.method == 'POST':
        # get value
        id_bipol = id
        posisi = request.form['posisi']
        kapasitas = request.form['kapasitas']
        current_datetime = datetime.now()
        waktu = str(current_datetime.strftime("%H:%M")) + ':00'
        # send put request posisi
        url = "http://localhost:8000/api/posisi/update/" + str(id)
        payload = json.dumps ({
            "id_bipol": id_bipol,
            "posisi": posisi,
            "waktu": waktu,
            "kapasitas": kapasitas
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("PUT", url, headers=headers, data=payload)
        print(response.text)
        # display posisiEdit page
        return redirect('../posisiRead')

@application.route('/posisiDelete/<int:id>')
def posisiDelete(id):
    # send delete request
    url = 'http://localhost:8000/api/posisi/delete/' + str(id)
    response = requests.request("DELETE", url)
    print(response.text)
    # display posisi 
    return redirect('../posisiRead')


@application.route('/login', methods=['GET', 'POST'])
def login():
    # send get request
    all_data_driver_str = (requests.get('http://localhost:8000/api/driver/')).text # ambil data dari api
    all_data_driver = json.loads(all_data_driver_str)["results"]
    if request.method == 'GET':
        # display login page
        return render_template('login.html')
    else:
        # get value
        username = request.form['user']
        password = request.form['passwd']
        # authentication admin
        if username == 'admin' and password == '123':
            # display dahsboardAdmin page
            return redirect('../jadwalRead')
        # authentication driver
        for i in all_data_driver:
            if i["username"] == username:
                if i["password"] == password:
                    auth = hashlib.md5(password.encode()).hexdigest()
                    print(auth)
                    # display dahsboardDriver page
                    return redirect('../dashboardDrivers/'+username+'/'+auth)
        # display login page
        return render_template('login.html')

@application.route('/logout', methods=['GET', 'POST'])
def logout():
    return redirect('/')

@application.route('/dashboardDriver/<string:username>', methods=['GET', 'POST'])
def dashboardDriver(username):
    # send get request
    all_data_driver_str = (requests.get('http://localhost:8000/api/driver/')).text # ambil data dari api
    all_data_driver = json.loads(all_data_driver_str)["results"]
    # send get request
    all_data_bipol_str = (requests.get('http://localhost:8000/api/bipol/')).text # ambil data dari api
    all_data_bipol = json.loads(all_data_bipol_str)["results"]
    for i in all_data_driver:
        if i['username'] == username:
            print(i['username'])
            print(username)
            driverid = i['id_driver']
            for j in all_data_bipol:
                if j['id_driver'] == driverid:
                    bipolid = j['id_bipol']
                    active1 = 'btn-primary'
                    active2 = 'btn-secondary'
                    print(bipolid)
                    return render_template('dashboardDriver.html', username=username, id=bipolid, active1=active1, active2=active2)
    return redirect('../')

# login dengan autentikasi
@application.route('/dashboardDrivers/<string:username>/<string:auth>', methods=['GET', 'POST'])
def dashboardDrivers(username,auth):
    # send get request
    all_data_driver_str = (requests.get('http://localhost:8000/api/driver/')).text # ambil data dari api
    all_data_driver = json.loads(all_data_driver_str)["results"]
    # send get request
    all_data_bipol_str = (requests.get('http://localhost:8000/api/bipol/')).text # ambil data dari api
    all_data_bipol = json.loads(all_data_bipol_str)["results"]
    for i in all_data_driver:
        if i['username'] == username:
            print(i['username'])
            auth_code = hashlib.md5(i['password'].encode()).hexdigest()
            print(username)
            driverid = i['id_driver']
            for j in all_data_bipol:
                if j['id_driver'] == driverid:
                    bipolid = j['id_bipol']
                    active1 = 'btn-primary'
                    active2 = 'btn-secondary'
                    print(bipolid)

                    # authentication
                    if auth_code == auth:
                        return render_template('dashboardDriver.html', username=username, id=bipolid, active1=active1, active2=active2)
    return redirect('../')


@application.route('/dashboardDriverOff/<string:username>/<int:id>', methods=['GET', 'POST'])
def dashboardDriverOff(username,id):
    payload = json.dumps ({
        "id_bipol": id,
        "posisi": '-',
        "waktu": '',
        "kapasitas": '-'
    })
    headers = {
        'Content-Type': 'application/json'
    }
    url = "http://localhost:8000/api/posisi/update/" + str(id)
    response = requests.request("PUT", url, headers=headers, data=payload)
    print(response.text)
    active1 = 'btn-secondary'
    active2 = 'btn-primary'
    able = 'disabled'
    return render_template('dashboardDriver.html', id=0, username=username, active1=active1, active2=active2, able=able)

@application.route('/<string:username>/<int:id>/<int:i>/<int:j>')
def updateDriver(username,id, i, j):
    data_posisi = (requests.get('http://localhost:8000/api/posisi/'+str(id))).text # ambil data dari api
    if id == 0:
        return redirect('../../dashboardDriverOff')
    elif i != 0:
        if i == 1:
            posisi = 'Stasiun UI'
        elif i == 2:
            posisi = 'Pondok Cina'
        else:
            posisi = 'PNJ'
        kapasitas = json.loads(data_posisi)["results"][0]['kapasitas']        
    else:
        if j == 1:
            kapasitas = 'Kosong'
        elif j == 2:
            kapasitas = 'Tersedia'
        else:
            kapasitas = 'Penuh'
        posisi = json.loads(data_posisi)["results"][0]['posisi']        
    current_datetime = datetime.now()
    waktu = str(current_datetime.strftime("%H:%M")) + ':00'
    payload = json.dumps ({
        "id_bipol": id,
        "posisi": posisi,
        "waktu": waktu,
        "kapasitas": kapasitas
    })
    headers = {
        'Content-Type': 'application/json'
    }
    url = "http://localhost:8000/api/posisi/update/" + str(id)
    response = requests.request("PUT", url, headers=headers, data=payload)
    print(response.text)
    
    return redirect('../../../dashboardDriver/'+username)





if __name__ == '__main__':
    application.run(debug=True)
