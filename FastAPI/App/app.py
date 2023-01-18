from fastapi import FastAPI, Response
from datetime import datetime, time, timedelta
from database import *
from schema import *
import mysql.connector
import uvicorn

api = FastAPI()
api.secret_key = "teuayanunyahoisina"

@api.get('/')
def index():
    return ({'title': 'API for Bipol Tracker', 'developer': 'Kelompok 2 - TMJ 3'})

# ============================================================================== #
#                               API Tes Individu                                 #
# ============================================================================== #

@api.post('/api/ganjil_genap')
async def cek_ganjil_genap(gage: GaGe):

    satu = gage.satu
    dua = gage.dua
    tiga = gage.tiga

    hasil_kali = satu * dua * tiga
    cek_gage = hasil_kali % 2

    if cek_gage == 0:
        return {"hasil": "genap"}
    else:
        return {"hasil": "ganjil"}

    '''
    contoh input
    {
        "satu": 10,
        "dua": 10,
        "tiga": 10
    }

    maka akan menghasilkan return
    {
        "hasil": "genap"
    }
    '''

# ============================================================================== #
#                                API for Driver                                  #
# ============================================================================== #

@api.get('/api/driver/')
async def driver_read():
    result = {}
    result['results'] = []
    sqlstr = f"SELECT * FROM `driver`"
    output_json = getMethod(sqlstr)

    for i in output_json:
        result['results'].append({'id_driver': i[0], 'nama': i[1], 'username': i[2], 'password': i[3]})

    print("Result:\n",result)
    return result

@api.get('/api/driver/{id}')
async def driver_readbyid(id: int):
    result = {}
    result['results'] = []
    sqlstr = f"SELECT * FROM `driver` WHERE `id_driver` = {id};"
    output_json = getMethod(sqlstr)

    for i in output_json: 
        result['results'].append({'id_driver': i[0], 'nama': i[1], 'username': i[2], 'password': i[3]})

    print("Result:\n",result)
    return result

@api.post('/api/driver/create')
async def driver_create(driver: Driver):
    sqlstr = f"INSERT INTO `driver` (`id_driver`, `nama`, `username`, `password`) VALUES ('{driver.id_driver}', '{driver.nama}', '{driver.username}', '{driver.password}') "
    output_status = postMethod(sqlstr)
    return output_status

@api.put('/api/driver/update/{id}')
async def driver_update(id: int, driver: Driver, response:Response):
    sqlstr = f"SELECT * FROM `driver` WHERE `id_driver` = {id};"
    output_json = getMethod(sqlstr)

    if output_json == []:
        response.status_code = 422
        return {"detail": "Data Not Found"}
    else:
        sqlstr = f"UPDATE `driver` SET  `id_driver` = '{driver.id_driver}', `nama` = '{driver.nama}', `username` = '{driver.username}', `password` = '{driver.password}' WHERE `driver`.`id_driver` = {id} "
        output_status = postMethod(sqlstr)
        return output_status

@api.delete('/api/driver/delete/{id}')
async def driver_delete(id: int, response:Response):
    sqlstr = f"SELECT * FROM `driver` WHERE `id_driver` = {id};"
    output_json = getMethod(sqlstr)

    if output_json == []:
        response.status_code = 422
        return {"detail": "Data Not Found"}
    else: 
        sqlstr = f"DELETE FROM `driver` WHERE `driver`.`id_driver` = {id} "
        output_status = postMethod(sqlstr)
        return output_status


# ============================================================================== #
#                                API for Bipol                                  #
# ============================================================================== #

@api.get('/api/bipol/')
async def bipol_read():
    result = {}
    result['results'] = []
    sqlstr = f"SELECT * FROM `bipol`"
    output_json = getMethod(sqlstr)

    for i in output_json:
        result['results'].append({'id_bipol': i[0], 'plat_nomor': i[1], 'id_driver': i[2]})

    print("Result:\n",result)
    return result

@api.get('/api/bipol/{id}')
async def bipol_readbyid(id: int):
    result = {}
    result['results'] = []
    sqlstr = f"SELECT * FROM `bipol` WHERE `id_bipol` = {id};"
    output_json = getMethod(sqlstr)

    for i in output_json: 
        result['results'].append({'id_bipol': i[0], 'plat_nomor': i[1], 'id_driver': i[2]})

    print("Result:\n",result)
    return result

@api.post('/api/bipol/create')
async def bipol_create(bipol: Bipol):
    sqlstr = f"INSERT INTO `bipol` (`id_bipol`, `plat_nomor`, `id_driver`) VALUES ('{bipol.id_bipol}', '{bipol.plat_nomor}', '{bipol.id_driver}') "
    output_status = postMethod(sqlstr)
    return output_status

@api.put('/api/bipol/update/{id}')
async def bipol_update(id: int, bipol: Bipol, response:Response):
    sqlstr = f"SELECT * FROM `bipol` WHERE `id_bipol` = {id};"
    output_json = getMethod(sqlstr)

    if output_json == []:
        response.status_code = 422
        return {"detail": "Data Not Found"}
    else:
        sqlstr = f"UPDATE `bipol` SET `id_bipol` = '{bipol.id_bipol}',  `plat_nomor` = '{bipol.plat_nomor}', `id_driver` = '{bipol.id_driver}' WHERE `bipol`.`id_bipol` = {id} "
        output_status = postMethod(sqlstr)
        return output_status

@api.delete('/api/bipol/delete/{id}')
async def bipol_delete(id: int, response:Response):
    sqlstr = f"SELECT * FROM `bipol` WHERE `id_bipol` = {id};"
    output_json = getMethod(sqlstr)

    if output_json == []:
        response.status_code = 422
        return {"detail": "Data Not Found"}
    else: 
        sqlstr = f"DELETE FROM `bipol` WHERE `bipol`.`id_bipol` = {id} "
        output_status = postMethod(sqlstr)
        return output_status


# ============================================================================== #
#                                API for Jadwal                                  #
# ============================================================================== #

@api.get('/api/jadwal/')
async def jadwal_read():
    result = {}
    result['results'] = []
    sqlstr = f"SELECT * FROM `jadwal`"
    output_json = getMethod(sqlstr)

    for i in output_json:
        result['results'].append({'id_jadwal': i[0], 'id_bipol': i[1], 'hari': i[2], 'waktu': str(i[3]), 'halte': i[4]})

    print("Result:\n",result)
    return result

@api.get('/api/jadwal/{id}')
async def jadwal_readbyid(id: int):
    result = {}
    result['results'] = []
    sqlstr = f"SELECT * FROM `jadwal` WHERE `id_jadwal` = {id};"
    output_json = getMethod(sqlstr)

    for i in output_json:
        result['results'].append({'id_jadwal': i[0], 'id_bipol': i[1], 'hari': i[2], 'waktu': str(i[3]), 'halte': i[4]})

    print("Result:\n",result)
    return result

@api.post('/api/jadwal/create')
async def jadwal_create(jadwal: Jadwal):
    sqlstr = f"INSERT INTO `jadwal` (`id_jadwal`, `id_bipol`, `hari`, `waktu`, `halte`) VALUES ('{jadwal.id_jadwal}', '{jadwal.id_bipol}', '{jadwal.hari}', '{jadwal.waktu}', '{jadwal.halte}') "
    print(sqlstr)
    output_status = postMethod(sqlstr)
    return output_status

@api.put('/api/jadwal/update/{id}')
async def jadwal_update(id: int, jadwal: Jadwal, response:Response):
    sqlstr = f"SELECT * FROM `jadwal` WHERE `id_jadwal` = {id};"
    output_json = getMethod(sqlstr)

    if output_json == []:
        response.status_code = 422
        return {"detail": "Data Not Found"}
    else:
        sqlstr = f"UPDATE `jadwal` SET `id_jadwal` = '{jadwal.id_jadwal}',  `id_bipol` = '{jadwal.id_bipol}', `hari` = '{jadwal.hari}', `waktu` = '{jadwal.waktu}', `halte` = '{jadwal.halte}' WHERE `jadwal`.`id_jadwal` = {id} "
        output_status = postMethod(sqlstr)
        return output_status

@api.delete('/api/jadwal/delete/{id}')
async def jadwal_delete(id: int, response:Response):
    sqlstr = f"SELECT * FROM `jadwal` WHERE `id_jadwal` = {id};"
    output_json = getMethod(sqlstr)

    if output_json == []:
        response.status_code = 422
        return {"detail": "Data Not Found"}
    else: 
        sqlstr = f"DELETE FROM `jadwal` WHERE `jadwal`.`id_jadwal` = {id} "
        output_status = postMethod(sqlstr)
        return output_status


# ============================================================================== #
#                                API for Posisi                                  #
# ============================================================================== #

@api.get('/api/posisi/')
async def posisi_read():
    result = {}
    result['results'] = []
    sqlstr = f"SELECT * FROM `posisi`"
    output_json = getMethod(sqlstr)

    for i in output_json:
        result['results'].append({'id_bipol': i[0], 'posisi': i[1], 'waktu': str(i[2]), 'kapasitas': i[3]})

    print("Result:\n",result)
    return result

@api.get('/api/posisi/{id}')
async def posisi_readbyid(id: int):
    result = {}
    result['results'] = []
    sqlstr = f"SELECT * FROM `posisi` WHERE `id_bipol` = {id};"
    output_json = getMethod(sqlstr)

    for i in output_json:
        result['results'].append({'id_bipol': i[0], 'posisi': i[1], 'waktu': str(i[2]), 'kapasitas': i[3]})

    print("Result:\n",result)
    return result

@api.post('/api/posisi/create')
async def posisi_create(posisi: Posisi):
    sqlstr = f"INSERT INTO `posisi` (`id_bipol`, `posisi`, `waktu`, `kapasitas`) VALUES ('{posisi.id_bipol}', '{posisi.posisi}', '{posisi.waktu}', '{posisi.kapasitas}') "
    print(sqlstr)
    output_status = postMethod(sqlstr)
    return output_status

@api.put('/api/posisi/update/{id}')
async def posisi_update(id: int, posisi: Posisi, response:Response):
    sqlstr = f"SELECT * FROM `posisi` WHERE `id_bipol` = {id};"
    output_json = getMethod(sqlstr)

    if output_json == []:
        response.status_code = 422
        return {"detail": "Data Not Found"}
    else:
        sqlstr = f"UPDATE `posisi` SET `posisi` = '{posisi.posisi}', `waktu` = '{posisi.waktu}', `kapasitas` = '{posisi.kapasitas}' WHERE `posisi`.`id_bipol` = {id} "
        output_status = postMethod(sqlstr)
        return output_status

@api.delete('/api/posisi/delete/{id}')
async def posisi_delete(id: int, response:Response):
    sqlstr = f"SELECT * FROM `posisi` WHERE `id_bipol` = {id};"
    output_json = getMethod(sqlstr)

    if output_json == []:
        response.status_code = 422
        return {"detail": "Data Not Found"}
    else: 
        sqlstr = f"DELETE FROM `posisi` WHERE `posisi`.`id_bipol` = {id} "
        output_status = postMethod(sqlstr)
        return output_status

if __name__ == '__main__':
    api.run(debug=True)