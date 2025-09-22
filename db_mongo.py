from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["persistencia_poliglota"]
locais = db["locais"]

def inserir_local(nome_local, cidade, latitude, longitude, descricao):
    documento = {
        "nome_local": nome_local,
        "cidade": cidade,
        "coordenadas": {"latitude": latitude, "longitude": longitude},
        "descricao": descricao
    }
    locais.insert_one(documento)

def listar_locais():
    return list(locais.find())