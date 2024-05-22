from machine import Pin, UART
import time

def add_header(listOfHexNumbers):
    header = [0xAA, 0xAA, 0xAA]
    return header + listOfHexNumbers

def string_to_hex(s):
    byte_data = s.encode('ascii')
    hex_string = ''.join(f'{b:02X}' for b in byte_data)
    hex_values = []
    for c in s:
        hex_value = "{:02X}".format(ord(c))
        hex_values.append(hex_value)
    return hex_values
    #return hex_string
    #return ' '.join(hex_values)

def hex_to_string(hex_string):
    # Convert hex string to bytes
    bytes_data = bytes.fromhex(hex_string)
    # Decode bytes to string
    original_string = bytes_data.decode('ascii')
    return original_string

uart0 = UART(0, baudrate=9600, parity=None, stop=1, bits=8, tx=Pin(0), rx=Pin(1), timeout=10) # the serial pins for USB
uart1 = UART(1, baudrate=9600, parity=None, stop=1, bits=8, tx=Pin(4), rx=Pin(5), timeout=10) # the serial pins for UART1
english_message = "hello"
hex_message = add_header(string_to_hex(english_message))
print(english_message, hex_message)
#uart1.write(bytes([0xAA, 0xAA, 0x20, 0x55]))
#english_message = hex_to_string(hex_message)
uart1.write(english_message)
time.sleep(0.1) # wait
rxData = bytes() # creates an empty bytes object 
rxData += uart0.read()
print(rxData)