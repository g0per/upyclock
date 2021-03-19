import network,utime,os

with open('wifi.dat','r') as archivowifiDB:
    guardados_list = archivowifiDB.readlines()

guardados = {}
contador = 1
numeroguardados = len(guardados_list)/2
for i in range(numeroguardados):
    guardados_list[i] = guardados_list[i].replace('\r','').replace('\n','')

for i in guardados_list[::2]:       # Lo convierte a diccionario
    guardados[i] = guardados_list[contador]
    contador +=2
print('{tamaño} SSIDs guardadas'.format(tamaño = len(guardados)))

wifi = network.WLAN(network.STA_IF)
wifi.active(False)
wifi.active(True)
disponibles = wifi.scan()
activas = []
for i in disponibles:
    if i[0].decode('ascii') in guardados:
        activas.append(i)
print('Conectando WiFi')
wifi.connect(activas[0][0].decode('ascii'),guardados[activas[0][0].decode('ascii')])
while not wifi.isconnected():
    print('Esperando conexión')
    utime.sleep(1)
print('Conectado a {SSID}'.format(SSID = activas[0][0].decode('ascii')))