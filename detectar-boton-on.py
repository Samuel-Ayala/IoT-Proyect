from sys import _current_frames
from adafruit_circuitplayground import cp
import time
import datetime
import json


# VENTANA DE TIEMPO PARA DEFINIR CADA CUANTO ENVIAR DATA
VENTANA = 10
temps = []
contador = 0
ultimo_valor = False

print("Starting ...")
inicio = time.time()
tiempo_temp = time.time()

while True:

    if cp.button_a and not ultimo_valor:
        cp.pixels[0] = (255,0,0)
        contador += 1
        # print(f"Valor del contador: {contador} a las {datetime.datetime.now()}")
        # cada vez que se aprieta el botón existe un rebote
        # en el voltaje que se descarga al presionar el botón
        # entonces cada pico de ese rebote se está considerando
        # como que se está presionando el botón. En general,
        # no solo pasa con pulsadores. Para esto se ACONDICIONA  
        # la señal; es decir que el rebote se eliminará parcialmente.
        time.sleep(0.1)
        # Debouncing -> es un método que permite retrasar la 
        # llamada de tu función hasta que no pasen los 
        # milisegundos que hayas definido,
        # desde la última vez que la función “rebotada” 
        # haya sido llamada 
        ultimo_valor = True
        # En este caso los datos que se envían constantemente,
        # se envían instante por instante, cuando verdaderamente
        # para un mejor análisis sería mejor enviar el dato acumulado
    
    elif not cp.button_a and ultimo_valor:
        cp.pixels[0] = (0,0,0)
        ultimo_valor = False
        # El encapsulamiento, forma en la que se enviará el paquete,
        # se debe incluir el timestamp y el valor (# de ciclos).

    # En caso se quiera nedir la temperatura como su comportamiento
    # no es variable, entonces no es necesario medirlo constantemente;
    # sin embargo, en caso se quiera medir cada cierto tiempo (min), entonces
    # ocurriría un error de resolución porque no se sabría que valor tomó
    # entre ese intervalo de tiempo
    # El promedio elimina las variaciones brusca (valores atípicos)
    
    if (time.time() - float(tiempo_temp)) >= 1.0:
        temps.append(cp.temperature)
        tiempo_temp = time.time()


    # Se creará un cliente mqtt (protocolo que implica enviar data
    # de todos los clientes subscribidos a un servidor, útil en comunicación
    # asíncrona y consume poco ancho de banda a diferencia de un cliente http)

    if (time.time() - inicio) >= float(VENTANA):
        temp_avg = 0
        for temp in temps:
            temp_avg += temp 
        temp_avg /= len(temps)

        data = {"cuenta": contador, 
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "temperatura": temp_avg}
        inicio = time.time()
        tiempo_temp = time.time()
        temps = []
        print(data)