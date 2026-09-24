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
#IMPORTO LIBRERÍAS
from datetime import datetime
import sys
import json
#===================LEO LOS DATOS Y LOS PASO A UN DICCIONARIO===================
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
#===================CONVIERTO LA FECHA Y HORA A DATETIME===================
def parsear_fecha_hora(fecha: str, hora: str) -> datetime: #Para hacer este codigo, tenía que darle un valor a cada mes ya que no reconoce a los meses en español
    """Convierte 'dd-mes-aaaa' y 'hh:mm' del SMN en un datetime."""
    mesesss= {
        "enero": 1, 
        "febrero": 2,
        "marzo": 3, 
        "abril": 4,
        "mayo": 5,
        "junio": 6, 
        "julio": 7, 
        "agosto": 8, 
        "septiembre": 9, 
        "octubre": 10, 
        "noviembre": 11,
        "diciembre": 12,
    }
    segmentos= fecha.strip().lower().split("-") #con strip limpiamos los segmentos en blanco u otros, y con split dividimos la cadena, para que a cada guion nos quede separado. 
    if len(segmentos) == 3: #Si la division del split nos da 3 valores, entonces asignamos al primero como día, al segundo como mes y al tercero como año
        dia= int(segmentos[0])
        mes= segmentos[1]
        año= int(segmentos[2])
        mesazo= mesesss.get(mes) #obtenemos el numero del mes que anteriormente subdividimos, con que cada segundo valor era parte de los meses
        if mesazo: #Si es un mes o existe entonces:
            fechita= f"{dia}-{mesazo}-{año} {hora}" #le damos el día, el mes, el año y la hora al codigo.
            return datetime.strptime(fechita, "%d-%m-%Y %H:%M") #Con la fecha y horas ya construidas, le asignamos el datetime, con los valores en ese orden

#===================FUNCION SEPARA VIENTO EN DIRECCION Y VELOCIDAD===================
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
    else: #Al final si lo agregue, mira si por esto me bajas un punto :(
        direccion= None
        velocidad= None    
    
    return {"direccion": direccion, "velocidad": velocidad}

#===================FUNCION CANTIDAD CIUDADES===================
def cantidad_ciudades(observaciones: dict) -> int: #Este fue el mas sencillo de todos creo, solo tengo que crear un contador, hacer un for a las claves de observaciones o sea a las ciudades o estaciones y por cada ciudad que haya aumentarle 1, dandonos como resultado el contador 
    contador= 0
    for estacion in observaciones.keys():
        contador += 1
    return contador

#===================FUNCION CANTIDAD DE CIUDADES CON TODOS LOS DATOS===================
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
#===================FUNCION AUXILIAR DE OBTENER VALOR===================
def obtener_valor(tupla): #Esta función intenta ayudar a top_n_ciudeades a indicarle al sort que ordene por magnitud numerica, o sea hay 2 partes, la clave, que es la ciudad, y después el indice que es el valor numerico, devolviendo solo la parte numerica.
    return tupla[1]
#===================FUNCION DE TOP CANTIDAD DE CIUDADES CON X DATOS===================
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

#===================FUNCION HORARIOS REPORTADOS===================
def horarios_reportados(observaciones: dict) -> list:
    """devuelve una lista de los horarios a los que las estaciones 
    reportaron en la observación dada. 
    La lista tendráhoras en el formato string "HH:MM",
    será sin repetir y ordenadas de menor a mayor"""
    horarios=[] #Creamos una lista de horarios
    for estacion, datos in observaciones.items(): #recorremos con for el nombre de la estacion y los datos
        hora= datos.get("hora") #le asignamos una variable a hora, que ya habíamos hecho en el campo 2 o 3 de leer observaciones
        if hora != "" and hora not in horarios: #Si la hora es distinta de literalmente nada, y también no esta en la lista de horarios, entonces:
            horarios.append(hora) #la agregamos a horarios
    horarios.sort() #ordenamos por numeracion los horarios
    return horarios 

CAMPOS_ESPERADOS= [
    "fecha", "hora", "estado", "vista", "temperatura", "sensacion", "humedad",
    "direccion", "velocidad", "presion"
]
#===================FUNCION REGISTRO CAMPOS FALTANTES===================
def campos_faltantes(datos, esperados=CAMPOS_ESPERADOS):
    faltantes= []
    for estacion, campos in datos.items():
        if isinstance(campos, dict):
            for campo in esperados:
                valor= campos.get(campo)
                if valor is None or valor == "" or str(valor).strip() =="No se calcula":
                    if campo not in faltantes:
                        faltantes.append(campo)
    return faltantes

#===================FUNCION CAMPOS FALTANTES===================  
def reporte_faltantes(datos, esperados= CAMPOS_ESPERADOS):
    reporte= {}
    for campo in esperados:
        con_falta = []
        for estacion, campos in datos.items():
            if isinstance(campos, dict):
                valor= campos.get(campo)
                if valor is None or valor == "" or str(valor).strip() == "No se calcula":
                    con_falta.append(estacion)
        reporte[campo]= {
            "cantidad": len(con_falta),
            "estaciones": con_falta
        }
    return reporte

#===================FUNCION CIUDAD CON TEMPERATURAS EXTREMAS===================
def temperatura_extrema(datos):
    validos= []
    for estacion, campos in datos.items():
        temp= campos.get("temperatura")
        if temp not in ("No se calcula", None):
            try:
                validos.append((estacion, float(temp)))
            except ValueError:
                continue
    temperaturas= [temp for estacion, temp in validos]
    maxima= max(temperaturas)
    minima= min(temperaturas)
    ciudades_max= [estacion for estacion, temp in validos if temp == maxima]
    ciudades_min= [estacion for estacion, temp in validos if temp == minima]
    
    return {
        "maxima": (maxima, ciudades_max),
        "minima": (minima, ciudades_min)
    }
    
#===================FUNCION CIUDAD CON VIENTOS EXTREMOS===================
def viento_extremo(datos):
    validos= []
    for estacion, campos in datos.items():
        vel= campos.get("velocidad")
        if vel not in ("No se calcula", None):
            try: 
                validos.append((estacion, float(vel)))
            except ValueError:
                continue
    vientitos= [viento for estacion, viento in validos]
    maximo= max(vientitos)
    minimo= min(vientitos)
    ciudades_max= [estacion for estacion, viento in validos if viento == maximo]
    ciudades_min= [estacion for estacion, viento in validos if viento == minimo]
    return {
        "maximo": (maximo, ciudades_max),
        "minimo": (minimo, ciudades_min)
    }        

#===================FUNCION IMPRIMIR EL RESTO DE FUNCIONES===================
def mostrar_resumen(observaciones: dict) -> None: #Aca directamente solo traímos los prints de cada función para hacer correr el codigo
    """Imprime por pantalla el resumen con todas las características calculadas. Usar n=5"""
    print("Diccionario General Ordenado y Prolijo")
    print(json.dumps(observaciones, indent= 4, ensure_ascii= False)) #El comando ensure_ascii en False, lo puse porque al correrlo quedaban los nombres medios raros, asi que le dije a la IA que los nombres se veían raros y como solucionarlo y me dijo que era porque bueno, el ensure ascii suele estar en verdadero, dandonos nombres raros, al ponerlo en falso, nos da los nombres verdaderos, sin afectar por así decirlo. )
    print("="*50)
    print("La cantidad de ciudades o estaciones es de: ",cantidad_ciudades(observaciones))
    print("="*50)
    print("La cantidad de ciudades con todos los valores es de: ", cantidad_ciudades_completas(observaciones))
    print("="*50)
    calores= top_n_ciudades(observaciones, campo= "temperatura", n= 7, descendente= True)
    print("Las Siete Ciudades mas Calurosas son")
    for estacion, temperatura in calores:
        print(f"{estacion}: {temperatura} °C")
    
    print("="*50)
    fríos= top_n_ciudades(observaciones, campo= "temperatura", n= 7, descendente= False)
    print("Las Siete Ciudades mas Frías son")
    for estacion, temperatura in fríos:
        print(f"{estacion}: {temperatura} °C")
    
    print("="*50)
    
    viento_desgraciado_molesto_insoportable= top_n_ciudades(observaciones, campo="velocidad", n=8, descendente= True)
    print("Las 8 ciudades con vientos más insoportables del país son: ")
    for estacion, velocidad in viento_desgraciado_molesto_insoportable:
        print(f"{estacion}: {velocidad} km/h")
    
    print("="*50)
    
    paz_calma_todo_lo_que_esta_bien= top_n_ciudades(observaciones, campo="velocidad", n=8, descendente= False)
    print("Las 8 ciudades con vientos más tranquilos del país son: ")
    for estacion, velocidad in paz_calma_todo_lo_que_esta_bien:
    
        print(f"{estacion}: {velocidad} km/h")
    
    print("="*80)
                
    for estacion, datos in observaciones.items():
        fecha_parseada= datos["fecha"]
        hora_parseada= datos["hora"]
        parsear= parsear_fecha_hora(fecha_parseada, hora_parseada)
        print("Las fecha y hora original, junto con la estacion es: ", estacion, fecha_parseada, hora_parseada)
        print("La fecha de la la estacion parseada y la estacion son las siguientes: ", estacion, parsear)
    
    print("="*80)
    
    horarios= horarios_reportados(observaciones)
    print("Horarios Reportados:")
    for hora in horarios: 
        print(hora)
        
    print("="*50)
        
    lista_faltantes = campos_faltantes(observaciones)
    if lista_faltantes:
        print(f"Campos con datos faltantes: {', '.join(lista_faltantes)}")
    else:
        print("Todos los campos tienen sus datos completos.")

    print("="*50)
    
    reporte= reporte_faltantes(observaciones)
    for campo, info in reporte.items():
        cant= info["cantidad"]
        estaciones= info["estaciones"]
        if cant > 0: 
            print(f"Campo '{campo}': faltan {cant} datos en {','.join(estaciones)}")
        else:
            print(f"campo '{campo}': completo en todas las estaciones")
            
    print("="*50)
            
    extremas= temperatura_extrema(observaciones)
    maxima= extremas["maxima"]
    minima= extremas["minima"]
    if maxima: 
        valor_max, ciudades_max = maxima
        print(f"Temperatura maxima: {valor_max}°C en {','.join(ciudades_max)}")
    if minima: 
        valor_min, ciudades_min= minima
        print(f"Temperatura minima: {valor_min}°C en {','.join(ciudades_min)}")

    print("="*80)
    
    extremos= viento_extremo(observaciones)
    maximo= extremos["maximo"]
    minimo= extremos["minimo"]
    if maximo:
        valor_max, ciudades_max= maximo
        print(f"Viento maximo: {valor_max}km/h en {','.join(ciudades_max)}")
    if minimo:
        valor_min, ciudades_min = minimo
        print(f"Viento minimo: {valor_min}km/h en {','.join(ciudades_min)}")
    
    print("="*80)
        
if __name__ == "__main__":
    if len(sys.argv) > 1:
        ruta= sys.argv[1]
    else:
        ruta= "estado_tiempo20260910.txt"
    observaciones= leer_observaciones(ruta)
    
    if observaciones:
        mostrar_resumen(observaciones)        
    else: 
        print(f"No se pudo procesar el archivo {ruta}...")
    