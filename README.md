# upyclock
Small micropython network-synced clock, using a ESP-WROOM32 and a HW069 I2C 4-digits 7-segments display.


# pinout

HW-069:
 * CLK: G2 (GPIO2)
 * DIO: G4 (GPIO4)
 * VCC: 3v3
 * GND: GND

# WLAN format
```
SSID1
SSID1pass
SSID2
SSID2pass
...
SSIDn
SSIDnpass
```
