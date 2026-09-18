#Aclaro que primero que todo no encuentro en la pagina metereologica 
#Observaciones actuales, donde debería incidir el archivo.
#por lo que primeramente lo haré con el archivo que nos da el profe
#en el repositorio de github, y luego lo haré con el archivo que se encuentra en la pagina metereologica.
#(si es que lo encuentro)
#gracias
#Segundo para aclarar, no se si falte a la clase, o si no lo vimos
#pero como el profe pide para el proyecto, cierto comando 
#para abrir el archivo y no se que cosa, lo saque de la inteligencia artificial,
#no para copiarme ni nada, solo para saber que era, y me dijo que
#necesitaba importar la libreria sys, para que el archivo ande con
#el comando :), muchas gracias por leer.
#algo así me dijo la inteligencia que se hacía:
#import sys
#sys.argv[1]
#ruta= sys.argv[1]
#with open(ruta, "r") as f:
#y ahí después se procesan los datos..
#intente hacer lo que esta al final del codigo para que al poner el
#comando, te deje verlo tranquilamente, pero al hacerlo, me salta un error
#de la consola de powershell, según la IA lo que sucedio fue eso, no sabría que hacer..
import sys
import json
def leer_observaciones(ruta:str) -> dict:
    diccionario= {}
    with open(ruta, "r") as climatico: 
        for linea in climatico: 
            limpita= linea.strip()
            if not limpita: 
                continue
            campos= [campo.strip() for campo in limpita.split(";")]
            estacion= campos[0]
            fecha= campos[1]
            hora= campos[2]
            estado= campos[3]
            vista= campos[4] #no se como se dice bien
            temperatura= campos[5]
            sensacion= campos[6]
            humedad= campos[7]
            viento= campos[8]
            presion= campos[9]
            partes_del_viento= viento.split()
            if len(partes_del_viento) >= 2:
                direccion= partes_del_viento[0]
                velocidad= partes_del_viento[1]
            elif len(partes_del_viento) == 1:
                direccion= partes_del_viento[0]
            else:
                direccion= None
                velocidad= None
            datos= {
                "fecha" : fecha, 
                "hora" : hora, 
                "estado": estado,
                "vista" : vista, 
                "temperatura": temperatura, 
                "sensacion": sensacion, 
                "humedad": humedad, 
                "direccion": direccion, 
                "velocidad": velocidad,
                "presion": presion
            }
            diccionario[estacion]= datos
    return diccionario
#if __name__ == "__main__":
#    ruta= sys.argv[1] 
ruta= "estado_tiempo20260910.txt"
observaciones= leer_observaciones(ruta) #o sino sirve el sys podría ser ruta= estado_tiempo20260910.txt
print(json.dumps(observaciones, indent= 4, ensure_ascii= False)) #El comando ensure_ascii en False, lo puse porque al correrlo quedaban los nombres medios raros, asi que le dije a la IA que los nombres se veían raros y como solucionarlo y me dijo que era porque bueno, el ensure ascii suele estar en verdadero, dandonos nombres raros, al ponerlo en falso, nos da los nombres verdaderos, sin afectar por así decirlo. 

def separar_viento(campo_viento: str) -> dict: #Esta función ya nos la pedía en la función anterior pero igual la voy a hacer, además de que es necesaria en la función anterior para dejar calculado la dirección y la velocidad.
    #Primero hay que agarrar la variable del viento, y separarla en partes con split()
    #para después si tiene dos partes, nombrar cada una, y si tiene una sola, nombrar la dirección y dejar la velocidad en None.
    #Y si, que no hice en el caso anterior porque me fije en la función y creo que si no me equivoco no le falta 
    #ninguna variable de direccion y velocidad o estado, por si acaso, y como tendría que ser, ya que en codigos muy largos se hace impredecible las variables
    #aca no lo hago para dejar las 2 partes, la principal, bien hecha, y esta
    #sin la funcionalidad de que si no tiene variable(direccion o velocidad), que sea nada.
    viento= campo_viento.split()
    if len(viento) >= 2:
        direccion= viento[0]
        velocidad= viento[1]
    elif len(viento) == 1:
        direccion= viento[0]
        velocidad= None
    return {"direccion": direccion, "velocidad": velocidad}
def cantidad_ciudades(observaciones: dict) -> int: #Este fue el mas sencillo de todos creo, solo tengo que crear un contador, hacer un for a las claves de observaciones o sea a las ciudades o estaciones y por cada ciudad que haya aumentarle 1, dandonos como resultado el contador 
    contador= 0
    for estacion in observaciones.keys():
        contador += 1
    return contador
print("La cantidad de ciudades o estaciones es de: ",cantidad_ciudades(observaciones))
def cantidad_ciudades_completas(observaciones: dict) -> int: #La función se parece bastante al algoritmo que tenía la función de contar numeros primos que vimos en el tp2, empezamos diciendo que todas son verdades, pero si cuentan con un detalle que las hace Falsas entonces la función se rompe y continua con la siguiente, así hasta encontrar a todas las ciudades con valores verdaderos, en el caso, lo hice también contando los casos de calma, o sea que cuando sea calma el valor será False, ya que lo saque directamente de la variable observaciones, pero en otro caso si quisiera poner como verdaderas las ciudades con estado "calma", tendría que sacarlo directamente del diccionario principal, sin alterar el viento en dirección y velocidad para que este tenga un valor
    llenas= 0
    for estacion, datos in observaciones.items():
        esta_completa= True
        for clave, valor in datos.items():
            if valor is None or valor == "" or valor == "No se calcula":
                esta_completa= False
                break
        if esta_completa: 
            llenas+= 1
    return llenas
print("La cantidad de ciudades con todos los valores es de: ", cantidad_ciudades_completas(observaciones))
def obtener_valor(tupla): #Esta función intenta ayudar a top_n_ciudeades a indicarle al sort que ordene por magnitud numerica, o sea hay 2 partes, la clave, que es la ciudad, y después el indice que es el valor numerico, devolviendo solo la parte numerica.
    return tupla[1]
def top_n_ciudades(observaciones: dict, campo: str, n: int, descendente: bool = True) -> list: #Hacer estas funciones me costó mucho más, primero tenía que empezar creando una lista, luego recorrer con .items(), para ir por cada ciudad y por cada subdiccionario, con get(campo) busca el valor solo del que esta asociado, como temperatura o incluso sensación termica. Luego con if valores, descarta los posibles valores que no sean numericos. Luego intenta convertir el string a float, si lo logra lo guarda en la lista, si no lo logra, que en esta parte tuve que repasar un poco el tp de los errores, usa except en caso de ValueError, y la función continua haciendose. Por ultimo, ordena la lisa de tuplas, usando el parametro descripto con anterioridad, y usando reverse= descendente, para saber si va de mayor a menor o de menor a mayor. El slicing recorta la lista desde el principio hasta la posicion n, pueden ser hasta n ciudades o elementos.
    lista=[]
    for estacion, datos in observaciones.items():
        valores= datos.get(campo)
        if valores is not None and valores != "No se calcula":
            try: 
                numerico= float(valores)
                lista.append((estacion, numerico))
            except ValueError:
                continue
    lista.sort(key=obtener_valor, reverse=descendente)
    return lista[:n]
calores= top_n_ciudades(observaciones, campo= "temperatura", n= 7, descendente= True)
print("Las Siete Ciudades mas Calurosas son")
for estacion, temperatura in calores:
    print(f"{estacion}: {temperatura} °C")
fríos= top_n_ciudades(observaciones, campo= "temperatura", n= 7, descendente= False)
print("Las Siete Ciudades mas Frías son")
for estacion, temperatura in fríos:
    print(f"{estacion}: {temperatura} °C")
viento_desgraciado_molesto_insoportable= top_n_ciudades(observaciones, campo="velocidad", n=8, descendente= True)
print("Las 8 ciudades con vientos más insoportables del país son: ")
for estacion, velocidad in viento_desgraciado_molesto_insoportable:
    print(f"{estacion}: {velocidad} km/h")
paz_calma_todo_lo_que_esta_bien= top_n_ciudades(observaciones, campo="velocidad", n=8, descendente= False)
print("Las 8 ciudades con vientos más tranquilos del país son: ")
for estacion, velocidad in paz_calma_todo_lo_que_esta_bien:
    print(f"{estacion}: {velocidad} km/h")
def mostrar_resumen(observaciones: dict) -> None:
    pass
