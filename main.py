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


def main(clk, dio):
    from main import Timechecker
    from boot import wifi_connect, wifi_drop
    import machine, utime

    wifi_drop()

    with open('debug.cfg','r') as debugcfg:
        debugmode = debugcfg.readlines()[0].lower() == 'true'
    print('debugmode = {debugmode}'.format(debugmode = debugmode))

    reloj=Timechecker()
    (cambio, lahora) = reloj.clcheck(1)
    _ = manda_horas(lahora, clk, dio)

    while True:
        (cambio, lahora) = reloj.clcheck(1)
        segundos = int(lahora[-1])
        if cambio:
            _ = manda_horas(lahora, clk, dio)
            
        if segundos <57:
            delay=57-segundos
        else:
            delay=0.1
        print('sleep {delay}s'.format(delay=delay+0.005))
        utime.sleep(0.005)

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

        print('RUN: main')
        self_test(CLK, DIO)
        clock=Reloj()
        sololog('ARRANQUE','main.py',clock.clhoracompleta())
        main(CLK, DIO)

    except Exception as e:
        try:
            #e=traceback.format_exception()
            print(e)
            logyreset(clock.clhoracompleta(), 'main.py',e)
        except Exception as e:
            #e=traceback.format_exception()
            logyreset2(e, 'main.py')