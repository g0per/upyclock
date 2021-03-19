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

def main():
    import time,ntptime
    from main import Pantalla
    from boot import hora,reloj

    display=Pantalla(2,4)
    (horas,minutos,segundos)=(int(hora(reloj())[0]),int(hora(reloj())[1]),int(hora(reloj())[2]))
    display.dibuja(horas,minutos)

    while True:
        time.sleep(0.1)
        if segundos != int(hora(reloj())[2]):
            (horasold,minutosold,segundosold) = (horas,minutos,segundos)
            (horas,minutos,segundos)=(int(hora(reloj())[0]),int(hora(reloj())[1]),int(hora(reloj())[2]))
            if horas != horasold or minutos != minutosold:
                display.dibuja(horas,minutos)
                print('{horas}:{minutos}'.format(horas=horas,minutos=minutos))
                if (hora,minutos) == ('00','00'):
                    ntptime.settime()

if __name__ == '__main__':
    try:
        main()

    except Exception as e:
        try:
            from boot import logyreset,horacompleta, reloj
            logyreset(horacompleta(reloj()),e)

        except Exception as f:
            logyreset2(f)

        reset()
