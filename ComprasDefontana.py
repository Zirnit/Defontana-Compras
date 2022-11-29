import requests
import FechasRelativas as FR
import HeadersKeys as HK

def lista_Compras():
    listaComprasAPI = "https://api.defontana.com/api/PurchaseOrder/List"
    listaComprasAPIQS = {"FromDate":FR.hace2Semanas,"ToDate":FR.hoy,"ItemsPerPage":"100","Page":"0"}
    listaComprasJson2 = requests.request("GET", listaComprasAPI, headers=HK.headersDefontana, params=listaComprasAPIQS).json()
    listaComprasAPIQS2 = {"FromDate":FR.hace2Semanas,"ToDate":FR.hoy,"ItemsPerPage":"100","Page":"1"}
    listaComprasJson = requests.request("GET", listaComprasAPI, headers=HK.headersDefontana, params=listaComprasAPIQS2).json()
    listaComprasDefon = {}
    for i in listaComprasJson["data"]:
        listaComprasDefon[str(i["number"])] = i["status"]
    for i in listaComprasJson2["data"]:
        listaComprasDefon[str(i["number"])] = i["status"]
    return listaComprasDefon

# Para obtener de la Compra solicitada: ("número de Compra - nombre", "detalle (código, cantidad, descripción)", "fecha de vencimiento")
def detalle_Compra(numero):
    listaComprasAPI = "https://api.defontana.com/api/PurchaseOrder/Get"
    listaComprasAPIQS = {"number": numero}
    ComprasJson = requests.request("GET", listaComprasAPI, headers=HK.headersDefontana, params=listaComprasAPIQS).json()["purchaseOrderData"]
    fechaEmision = ComprasJson["emissionDate"][:19]
    fechaRecepcion = ComprasJson["receiptDate"][:10]+"T11:30:00"
    proveedor = ComprasJson["providerInfo"]["name"]
    direccionProveedor = ComprasJson["providerInfo"]["address"]
    comuna = ComprasJson["dispatchDistrict"]
    despacho = ComprasJson["dispatchAddress"]
    glosa = ComprasJson["comment"]
    nombre = f"{numero} - {proveedor}"
    detalle = ["Productos:\n"]
    for i in ComprasJson["purchaseOrderDetail"]:
        detalle.append(i["productId"])
        detalle.append("\t")
        detalle.append(str(i["quantity"]))
        detalle.append("\t")
        detalle.append(i["product"]["description"])
        if i["comment"]:
            detalle.append("\nComentario: ")
            detalle.append(i["comment"])
        detalle.append("\n")
    detalle.append(glosa)
    detalle = "".join(detalle)
    return nombre, detalle, fechaEmision, fechaRecepcion, direccionProveedor, comuna, despacho
