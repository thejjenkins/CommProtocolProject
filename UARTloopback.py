from machine import Pin, UART
import time

uart0 = UART(0, baudrate=9600, parity=None, stop=1, bits=8, tx=Pin(0), rx=Pin(1), timeout=10) # the serial pins for USB
uart1 = UART(1, baudrate=9600, parity=None, stop=1, bits=8, tx=Pin(4), rx=Pin(5), timeout=10) # the serial pins for UART1
uart1.write('hello\n') # sent by Pin(4)
time.sleep(0.1) # wait
rxData = bytes() # creates an empty bytes object 
while uart0.any() > 0: # received by Pin(1)
    rxData += uart0.read(1) # add received byte to byte object 
    print(rxData.decode('ascii')) # print decoded ascii characters