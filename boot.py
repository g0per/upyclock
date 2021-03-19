#! upython
# coding=utf-8
#

def wifi_connect():
    ''' Network setup'''
    #print('RUN: boot.wifi_connect')

    import network,time,os,ntptime

    if 'wifi.dat' in os.listdir():      # Lee fichero de contraseñas
        with open('wifi.dat','r') as archivowifiDB:
            guardados_list = archivowifiDB.readlines()

        if len(guardados_list) % 2 == 1:
            print('Comprobar formato de wifi.dat\n\t El formato correcto es:\n\t\tSSID1\n\t\tpass1\n\t\tSSID2\n\t\tpass2\n\t\tetc')
        else:
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
            if not wifi.isconnected():      # Escanea, y comprueba en orden si están guardados credenciales para conectarse
                disponibles = wifi.scan()
                activas = []
                for i in disponibles:
                    if i[0].decode('ascii') in guardados:
                        activas.append(i)
                if len(activas) == 0:
                    print('ERROR: Redes configuradas no disponibles.')
                else:
                    print('Conectando WiFi')
                    wifi.connect(activas[0][0].decode('ascii'),guardados[activas[0][0].decode('ascii')])
                    while not wifi.isconnected():
                        print('Esperando conexión')
                        time.sleep(1)
            ntptime.settime()

def memoria():
    ''' Free memory'''
    import gc
    gc.collect
    memoria = gc.mem_free()
    print('Memoria disponible: {memoria}'.format(memoria = memoria))

def reloj():
    import time
    currenttime = []
    for i in time.localtime(time.time())[:6]:
        i = str(i)
        currenttime.append(i)
    with open('timezone.dat','r') as archivotimezone:
        timezone = archivotimezone.readlines()[0]
    currenttime[3] = str(int(currenttime[3])+int(timezone))
    if currenttime[3] == '24':
        currenttime[3] = '00'

    for i in range(1,6):
        if len(currenttime[i]) == 1:
            currenttime[i] = '0'+currenttime[i]
    return currenttime

def horacompleta(str_reloj):
    texto = str_reloj[0]+str_reloj[1]+str_reloj[2] +' '+ str_reloj[3]+str_reloj[4] +':'+ str_reloj[5]
    print('Hora: {texto}'.format(texto=texto))
    return texto

def hora(str_reloj):
    return (str_reloj[3],str_reloj[4],str_reloj[5])

def logyreset(horadelfallo,error):
    from machine import reset
    with open('log.dat','ab') as archivo:
        texto = horacompleta(reloj()) + ' boot.py ' + str(error)
        archivo.write(texto)
    reset()

def logyreset2(error):
    from machine import reset
    with open('log.dat','ab') as archivo:
        texto = 'ERROR EN HORACOMPLETA PARA LOG - boot.py ' + str(error)
        archivo.write(texto)
    reset()

def main():
    try:
        print('RUN: boot')
        memoria()
        wifi_connect()
        horacompleta(reloj())
    except Exception as e:
        try:
            logyreset(horacompleta(reloj()),e)
        except Exception as f:
            logyreset2(f)
if __name__ == '__main__':
    main()
