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
    def clcheck(self, posicion):
        nuevahora = self.clock.clhora()
        cambio = (nuevahora[:posicion+1] != self.hora[:posicion+1])   # Comprueba posición enviada. 0=h, 1=min, 2=s
        if cambio:
            self.hora = nuevahora
        print(cambio,nuevahora)
        return (cambio,nuevahora)   # aunque diga que no cambia y self.hora siga igual, los segundos sí que varían. Se retorna con la hora actual


def manda_horas(conjunto_resultado,clk,dio):
    import utime
    from main import Pantalla
    display=Pantalla(clk,dio)
    
    (horas, minutos, segundos) = conjunto_resultado
    print('{horas}:{minutos}:{segundos}'.format(horas=horas, minutos=minutos, segundos=segundos))
    (horas, minutos, segundos) = (int(horas), int(minutos), int(segundos))
    display.dibuja(horas, minutos)

    return (horas, minutos, segundos)


def self_test(clk,dio):
    from main import Pantalla
    import utime
    display=Pantalla(clk,dio)

    test = [
    ('88','88','88'),
    ('00','00','00')]

    for i in test:
        _=manda_horas(i,clk,dio)
        utime.sleep(1)

    del display


class Gestor:
    def __init__(self,botonPINs):
        global interrumpe
        interrumpe = False

        (horasPIN, minutosPIN, setupPIN) = botonPINs

        import machine

        self.horas = machine.Pin(horasPIN,machine.Pin.IN,machine.Pin.PULL_DOWN)
        self.minutos = machine.Pin(minutosPIN,machine.Pin.IN,machine.Pin.PULL_DOWN)
        self.setup = machine.Pin(setupPIN,machine.Pin.IN,machine.Pin.PULL_DOWN)

    def ciclo(self):
        import utime

        while True:
            interrumpe = self.setup.value()
            if interrumpe:
                print('Setup ON')




def main(pantallaPINs, botonPINs):
    from main import Timechecker
    from boot import wifi_connect, wifi_drop
    import machine, utime, _thread

    (clk, dio) = pantallaPINs

    wifi_drop()

    global debugmode, botonsetup
    botonsetup = False

    interrupciones = Gestor(botonPINs)
    _thread.start_new_thread(interrupciones.ciclo,())


    with open('debug.cfg','r') as debugcfg:
        debugmode = debugcfg.readlines()[0].lower() == 'true'
    print('debugmode = {debugmode}'.format(debugmode = debugmode))

    reloj=Timechecker()
    (cambio, lahora) = reloj.clcheck(1)
    _ = manda_horas(lahora, clk, dio)

    delaytext=0.005

    while True:
        (cambio, lahora) = reloj.clcheck(1)
        if cambio:
            _ = manda_horas(lahora, clk, dio)
            minutos = lahora[1]
            if int(minutos) == 50:
                wifi_connect()
                wifi_drop()
                (cambio, lahora) = reloj.clcheck(1)
        segundos = int(lahora[-1])

            
        if segundos <57:
            delay=57-segundos-delaytext
        else:
            delay=0.1-delaytext
        #delay=0.1-delaytext
        print('sleep {delay}s'.format(delay=delay+delaytext))
        utime.sleep(delaytext)

        if debugmode:
            utime.sleep(delay)
        else:
            delay=int(delay*1000)
            machine.lightsleep(delay)
        del delay


if __name__ == '__main__':
    try:
        from boot import Reloj, logyreset, logyreset2, sololog
        #import traceback

        CLK = 2
        DIO = 4

        horasPIN = 14
        minutosPIN = 27
        setupPIN = 12

        pantallaPINs = (CLK, DIO)
        botonPINs = (horasPIN, minutosPIN, setupPIN)

        print('RUN: main')
        self_test(CLK, DIO)
        clock=Reloj()
        sololog('ARRANQUE','main.py',clock.clhoracompleta())
        main(pantallaPINs, botonPINs)

    except Exception as e:
        try:
            #e=traceback.format_exception()
            print(e)
            logyreset(clock.clhoracompleta(), 'main.py',e)
        except Exception as e:
            #e=traceback.format_exception()
            logyreset2(e, 'main.py')