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
        time.sleep(0.1)
        # para acondicionar la función y evitar el rebote de voltaje
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