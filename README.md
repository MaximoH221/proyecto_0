El proyecto, terminado en Analisis_SMN.py, trata sobre iterar sobre un archivo.txt, en este caso estado_tiempo20260910.txt, que contiene
datos sobre el clima en diversas ciudades de la Argentina, el archivo ordena de forma prolija y ordenada, cada ciudad con sus respectivos
datos climaticos, y sobre todo con el viento separado en direccion y velocidad, siendo un total de 10 modulos sobre datos del clima, como lo son:
fecha, hora, estado, vista, temperatura, sensacion, humedad, direccion, velocidad, presion.
Además de eso hace cosas como parsear la fecha y hora a datetime, un contador del total de ciudades/estaciones, un contador de todas las ciudades
con datos completos, obtiene las 5 ciudades con más, etc, puede ser temperatura, velocidad del viento, o incluso con menos, devuelve los 
horarios en que se reportaron los datos climaticos, registra que campos tienen datos faltantes y cuales no, y en que estaciones estan los campos
faltantes y la temperatura y viento maximo y minimo.
Para cuando este subido esto aclaro que no se si le habre sacado el json por motivos tecnicos, pero lo mas seguro es que sí, ya que no se imprimen
todas las ciudades/estaciones con sus datos. 
Para ejecutar el proyecto hay que hacer desde la terminal python Analisis_SMN y el parametro estado_tiempo20260910 al lado, con eso se corre el trabajo
Luego hay que entrar a la pagina del servicio metereologico, aqui dejo el link: https://www.smn.gob.ar/descarga-de-datos , hay que aceptar
los terminos y condiciones y descargar el estado del tiempo presente, una vez hecho eso, dentro del zip hay que dar click derecho y darle a 
"extraer aqui" una vez obtenido te da el archivo.txt listo para emplear en el programa
