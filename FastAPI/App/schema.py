from pydantic import BaseModel
# from datetime import datetime, time, timedelta

class Driver(BaseModel):
    id_driver: int
    nama: str
    username: str
    password: str

class Bipol(BaseModel):
    id_bipol: int
    plat_nomor: str
    id_driver: int

class Jadwal(BaseModel):
    id_jadwal: int
    id_bipol: int
    hari: str
    waktu: str
    halte: str

class Posisi(BaseModel):
    id_bipol: int
    posisi: str
    waktu: str
    kapasitas: str

# schema tes individu
class GaGe(BaseModel):
    satu: int
    dua: int
    tiga: int