import ComprasDefontana as CD
import TarjetasTrello as TT
import FechasRelativas as FR
import positionstack as PS
import time
from datetime import datetime
from importlib import reload

# Consultar Compras en defontana
def obtenerCompras():
    ComprasDefontana = CD.lista_Compras()
    return ComprasDefontana

# Consultar tarjetas existentes en Trello
def obtenerTarjetas():
    tarjetasTrello = TT.lista_tarjetas_trello()
    return tarjetasTrello

# Comparar si existe en Trello y crea tarjeta, o actualiza su estado
def cargar_trello(numero, Compras, tarjetas):
    try:
        nombre, detalle, fechaEmision, fechaRecepcion, direccionProveedor, comuna, despacho = CD.detalle_Compra(numero)
    except:
        print(numero, Compras[numero], "Vacío")
        return None
    else:
        if numero not in tarjetas and datetime.strptime(fechaEmision, "%Y-%m-%dT%H:%M:%S").date() > FR.hace2Semanas:
            if despacho == "Calle Poeta Pedro Prado 1689 oficina 06":
                etiqueta = ""
                lista = TT.ordenes_idList
                coordenada = ""
            else:
                etiqueta = ""
                lista = TT.buscar_idList
                coordenada, latitude, longitude= PS.obtenerCoordenadas(despacho, comuna)
            TT.post_trello(nombre, detalle, fechaEmision, fechaRecepcion, coordenada, idList=lista)
        if numero in tarjetas:
            estado = Compras[numero]
            if estado == "Aprobado" and fechaRecepcion == FR.hoy:
                TT.mod_trello(tarjetas[numero], "false", TT.en_ruta_idList)
            elif estado == "Aprobado":
                pass
            elif estado == "Cerrado":
                TT.mod_trello(tarjetas[numero], "false", TT.recibidos_idList)
            elif datetime.strptime(fechaEmision, "%Y-%m-%dT%H:%M:%S").date() < FR.hace1Semana and estado == "Cerrado":
                elimina_Trello(numero, tarjetas)
            else:
                print(numero, Compras[numero])

# Archiva tarjetas Trello
def elimina_Trello(numero, tarjetas):
    TT.mod_trello(tarjetas[numero], "true", TT.recibidos_idList)

# Archiva tarjetas Trello que no estén en el listado de Compras pendientes
def elimina_Trello2(Compras, tarjetas):
    for numero in tarjetas:
        if numero not in Compras:
            elimina_Trello(numero, tarjetas)

# Función principal, que ejecuta las funciones necesarias para correr el código
def principal():
    Compras = obtenerCompras()
    tarjetas = obtenerTarjetas()
    for item in Compras:
        cargar_trello(item, Compras, tarjetas)
    elimina_Trello2(Compras, tarjetas)

# Bucle que mantiene el programa actualizándose   
while True:
    print("Actualizando...")
    try:
        principal()
    except Exception as e:
        print(e)
    print("Actualización: ", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    time.sleep(300) # Tiempo de espera: 5 minutos
    # Siempre que esté corriendo en el servidor, no vale la pena tener el tiempo de espera
    FR = reload(FR)
# principal() #Test