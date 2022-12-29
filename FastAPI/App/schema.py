from pydantic import BaseModel
# from datetime import datetime, time, timedelta

class Driver(BaseModel):
    nama: str
    username: str
    password: str

class Bipol(BaseModel):
    plat_nomor: str
    id_driver: int

class Jadwal(BaseModel):
    id_bipol: int
    hari: str
    waktu: str
    halte: str

class Posisi(BaseModel):
    id_bipol: int
    posisi: str
    waktu: str
    kapasitas: str