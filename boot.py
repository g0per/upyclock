#! upython
# coding=utf-8
#

def wifi_connect():
    ''' Network setup'''
    #print('RUN: boot.wifi_connect')

    import network,utime,os,ntptime

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
                    print('ERROR: Redes configuradas no disponibles')
                else:
                    print('Conectando WiFi')
                    wifi.connect(activas[0][0].decode('ascii'),guardados[activas[0][0].decode('ascii')])
                    while not wifi.isconnected():
                        print('Esperando conexión')
                        utime.sleep(1)
            print('Conectado a {SSID}'.format(SSID = activas[0][0].decode('ascii')))
            ntptime.settime()

def wifi_drop():
    import network

    print('Soltando conexión')
    wifi = network.WLAN(network.STA_IF)
    if wifi.isconnected():
        wifi.active(False)

def memoria():
    ''' Free memory'''
    import gc
    gc.collect
    memoria = gc.mem_free()
    print('Memoria disponible: {memoria}'.format(memoria = memoria))

class Reloj:
    def __init__(self):
        import utime
        with open('timezone.dat','r') as archivotimezone:
            self.timezone = archivotimezone.readlines()[0]

    def clupdate(self):
        import utime
        self.currenttime = []
        for i in utime.localtime()[:6]:
            i = str(i)
            self.currenttime.append(i)
        self.currenttime[3] = str(int(self.currenttime[3])+int(self.timezone))
        if self.currenttime[3] == '24':
            self.currenttime[3] = '00'

        for i in range(1,6):
            if len(self.currenttime[i]) == 1:
                self.currenttime[i] = '0'+self.currenttime[i]

    def clhora(self):
        self.clupdate()
        return (self.currenttime[3], self.currenttime[4],self.currenttime[5])

    def clhoracompleta(self):
        self.clupdate()
        texto = self.currenttime[0]+self.currenttime[1]+self.currenttime[2] +' '+self.currenttime[3]+self.currenttime[4] +':'+ self.currenttime[5]
        return texto

    def __str__(self):
        return self.clhoracompleta()

    def cladjust(self,posicion):
        if posicion == 'h':
            if self.currenttime[3] == '23':
                self.currenttime[3] = '00'
                return
            else:
                pos = 3
        elif posicion == 'm':
            if self.currenttime[4] == '59':
                self.currenttime[4] = '00'
            else:
                pos = 4
        else:
            return
        self.currenttime[posicion] = str(int(self.currenttime[posicion])+1)


def logyreset(horadelfallo, funcion, error):
    from machine import reset
    import utime

    with open('log.dat','ab') as archivo:
        texto = 'LR '+' '+horadelfallo+' '+funcion+' '+ str(error) + '\n'
        archivo.write(texto)
    print(texto)
    utime.sleep(5)
    reset()

def logyreset2(error,funcion):
    from machine import reset
    import utime

    with open('log.dat','ab') as archivo:
        texto = 'LR2 ERROR EN HORACOMPLETA PARA LOG - '+funcion+' - '+ str(error) + '\n'
        archivo.write(texto)
    print(texto)
    utime.sleep(5)
    reset()

def sololog(msg, funcion, horadellog):
    with open('log.dat','ab') as archivo:
        texto = horadellog +' '+funcion+' '+ str(msg) + '\n'
        archivo.write(texto)
    print(texto)


def main():
    try:
        #import traceback

        print('RUN: boot')
        global clock

        clock=Reloj()
        sololog('ARRANQUE','boot.py',clock.clhoracompleta())
        memoria()
        print(clock)
        wifi_connect()
        print(clock)
    except Exception as e:
        try:
            #e=traceback.format_exc()
            print(e)
            logyreset(clock.clhoracompleta(),'boot.py', e)
        except Exception as e:
            #e=traceback.format_exc()
            logyreset2(e,'boot.py')

if __name__ == '__main__':
    main()
