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
    import utime
    reloj=Timechecker()

    global actualizar_Pantalla
    global resultado

    actualizar_Pantalla=False
    resultado=('00','00','00')

    while True:
        (actualizar_Pantalla,resultado) = reloj.clcheck()
        utime.sleep(0.1)

def main():
    import utime,ntptime, _thread
    from main import Pantalla

    _thread.start_new_thread(seguimiento_reloj,())

    utime.sleep(2)

    display=Pantalla(2,4)
    (horas,minutos,segundos)=(int(resultado[0]),int(resultado[1]),int(resultado[2]))
    print('{horas}:{minutos}'.format(horas=horas,minutos=minutos))
    display.dibuja(horas,minutos)

    while True:
        if actualizar_Pantalla:
            if (horas,minutos)!=(int(resultado[0]),int(resultado[1])):
                (horas,minutos,segundos)=(int(resultado[0]),int(resultado[1]),int(resultado[2]))
                display.dibuja(horas, minutos)
                print('{horas}:{minutos}'.format(horas=horas,minutos=minutos))

                if (horas,minutos) == ('00','00'):
                    ntptime.settime()

if __name__ == '__main__':
    try:
        from boot import Reloj, logyreset, logyreset2
        #import traceback

        print('RUN: main')
        clock=Reloj()
        main()

    except Exception as e:
        try:
            #e=traceback.format_exception()
            print(e)
            logyreset(clock.clhoracompleta(), 'main.py',e)
        except Exception as e:
            #e=traceback.format_exception()
            logyreset2(e, 'main.py')