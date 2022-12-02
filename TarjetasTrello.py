import requests
import HeadersKeys as HK

# Lista idList de Trello board "Compras"
ordenes_idList = "6373dd6176f3a50ca68a4a98" # Órdenes de compra
buscar_idList = "6373e63f22f54803ee382440" # Ir a buscar
en_ruta_idList = "6373dd6bc5df92016c7705fe" # En ruta
recibidos_idList = "6373dd910ea7d20154813028" # Monsalve

# Etiquetas de Trello board "Compras"

# Create Trello card
def post_trello(nombre, detalle, fechaEmision, fechaRecepcion, coordenada="", idList=ordenes_idList):
    trelloCard = "https://api.trello.com/1/cards" # Dirección API
    TrelloQS = {
    "key":HK.Tkey,
    "token":HK.Ttoken,
    "idList":idList,        # Lista en Trello
    "name":nombre,          # Nombre de la tarjeta
    "desc":detalle,         # Descripción de la tarjeta
    "pos":"top",            # Posición en la cual se crea la tarjeta (top, bottom, or a positive float)
    "start": fechaEmision,  # Fecha de "comienzo" de la tarjeta  
    "due": fechaRecepcion,  # Fecha de "caducidad" de la tarjeta
    #"address": direccion,
    #"locationName": comuna,
    "coordinates":coordenada,
    # "idLabels":idLabels
    } 
    requests.request("POST", trelloCard, headers=HK.trelloHeaders, params=TrelloQS)

# Para obtener las ID de las tarjetas de Trello
def lista_tarjetas_trello():
    tarjetasTrelloURL = "https://api.trello.com/1/boards/6373dcefc0f5a70075826fea/cards" # filter Valid Values: all, closed, none, open, visible.
    IDtarjetasTrello = {}
    requestTarjetasTrello = requests.request(
    "GET",
    tarjetasTrelloURL,
    headers=HK.trelloHeaders,
    params=HK.trelloQuery
    ).json()
    for i in requestTarjetasTrello:
        espacio = i["name"].index(" ")
        IDtarjetasTrello[i["name"][:espacio]] = i["id"]
    return IDtarjetasTrello

# Modificar tarjeta Trello
def mod_trello(cardID, closed, idList=ordenes_idList):
    trelloCard = f"https://api.trello.com/1/cards/{cardID}" # Dirección API
    querystring = {
    "key":HK.Tkey,
    "token":HK.Ttoken,
    "closed": closed,
    "idList": idList,
    # "idLabels": idLabel
    }
    requests.put(trelloCard, headers=HK.trelloHeaders, params=querystring)
