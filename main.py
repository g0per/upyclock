#! upython
# coding=utf-8
#

class Pantalla:
    def __init__(self,clk,dio,brillo=7):
        import tm1637
        from machine import Pin
        self.brillo = brillo
        self.tm = tm1637.TM1637(clk=Pin(clk),dio=Pin(dio),brightness=self.brillo)
        self.tm.write([0,0,0,0])

    def dibuja(self,numero1,numero2):
        self.tm.write([0,0,0,0])
        self.tm.numbers(numero1,numero2)

    def togglebrillo(self):
        if self.brillo == 7:
            self.brillo = 0
        else:
            self.brillo += 1

class Timechecker:
    def __init__(self):
        from boot import Reloj
        self.clock=Reloj()
        self.hora = self.clock.clhora()
    def clcheck(self):
        nuevahora = self.clock.clhora()
        cambio = (nuevahora[:2] != self.hora[:2])
        if cambio:
            self.hora = nuevahora
        return (cambio,self.hora)

def seguimiento_reloj():
    import utime, machine
    reloj=Timechecker()

    global actualizar_Pantalla
    global resultado

    with open('debug.cfg','r') as settingscfg:
            settings = settingscfg.readlines()
    debugmode = settings[0].lower == 'true'
    print('debugmode = {debugmode}'.format(debugmode = debugmode))

    actualizar_Pantalla=False
    resultado=('00','00','00')
    rtc = machine.RTC()

    while True:
        (actualizar_Pantalla,resultado) = reloj.clcheck()
        if debugmode:
            utime.sleep(0.1)
        else:
            machine.lightsleep(100)


def manda_horas(conjunto_resultado):
    from main import Pantalla
    display=Pantalla(2,4)
    
    (horas, minutos, segundos) = conjunto_resultado
    print('{horas}:{minutos}'.format(horas=horas, minutos=minutos))
    (horas, minutos, segundos) = (int(horas), int(minutos), int(segundos))
    display.dibuja(horas, minutos)

    return (horas, minutos, segundos)


def main():
    import utime, _thread
    from main import Pantalla
    from boot import wifi_connect, wifi_drop, sololog

    _thread.start_new_thread(seguimiento_reloj,())
    wifi_drop()

    utime.sleep(2)

    (horas, minutos, segundos)= manda_horas(resultado)
    i=0

    while True:
        if actualizar_Pantalla:
            if (horas,minutos)!=(int(resultado[0]),int(resultado[1])):
                (horas, minutos, segundos)= manda_horas(resultado)

                if minutos == 0 and horas in (0,2,3):
                    print('Poniendo en hora...')
                    try:
                        wifi_connect()
                        wifi_drop()
                    except Exception as e:
                        msg = 'Error al conectar para poner en hora: {e}\n\tNo se sincroniza la hora'.format(e = e)
                        print(msg)
                        sololog(msg, 'main.py_SYNC_IF')
            utime.sleep(0.8)
        else:
            utime.sleep(0.021)

if __name__ == '__main__':
    try:
        from boot import Reloj, logyreset, logyreset2, sololog
        #import traceback

        print('RUN: main')
        clock=Reloj()
        sololog('ARRANQUE','main.py', clock)
        main()

    except Exception as e:
        try:
            #e=traceback.format_exception()
            print(e)
            logyreset(clock.clhoracompleta(), 'main.py',e, clock)
        except Exception as e:
            #e=traceback.format_exception()
            logyreset2(e, 'main.py')