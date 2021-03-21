# upyclock
Small micropython network-synced clock, using a ESP-WROOM32 and a HW069 I2C 4-digits 7-segments display.

## pinout

HW-069:
 * CLK: G2 (GPIO2)
 * DIO: G4 (GPIO4)
 * VCC: 3v3
 * GND: GND

## Minimum required files & directory scheme
All those files into microcontroller's root folder:

* /boot.py
* /main.py
* /tm1637.py
* /wifi.dat -> properly filled in
* /log.dat
* /timezone.dat properly filled in
* /debug.cfg -> properly filled in

### wifi.dat
Example:

```
SSID1
SSID1pass
SSID2
SSID2pass
```

### timezone.dat
Defaults to UTC. Add an integer for an integer amount of hours timezone delta.

Example:

```
1
```

Means UTC+1

### debug.cfg
Boolean value for selecting either lightsleep or normal (power-hungrier) utime.sleep(), so serial console doesnt get disrupted. Anything other than 'true' chooses lightsleep.

Example:

```
False
```

Selects lightsleep.
