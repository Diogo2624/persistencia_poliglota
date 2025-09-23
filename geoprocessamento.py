from geopy.distance import geodesic

def calcular_distancia(coord1, coord2):
    return geodesic(coord1, coord2).km

def locais_proximos(lista_locais, coord_ref, raio_km=10):
    proximos = []
    for local in lista_locais:
        lat = local["coordenadas"]["latitude"]
        lon = local["coordenadas"]["longitude"]
        distancia = calcular_distancia(coord_ref, (lat, lon))
        if distancia <= raio_km:
            proximos.append((local["nome_local"], distancia))
    return proximos