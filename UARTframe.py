from machine import Pin, UART
import time

"""
The goal of this code is to create frames.
The header will take influence from MIN which has three 0xAA to indicate the beginning of a frame.
I do not know about checksums yet so I will just do some experiments with a header, payload, and ending byte.
"""

def add_header(listOfHexNumbers):
    header = [0xAA, 0xAA, 0xAA]
    return header + listOfHexNumbers
headers_seen = 0

def add_ending(listOfHexNumbers):
    ending = [0xAA]
    return listOfHexNumbers + ending

def string_to_hex(s):
    ############ Method 1: returns a hex string ################
    # byte_data = s.encode('ascii')
    # hex_string = ''.join(f'{b:02X}' for b in byte_data)
    # return hex_string
    ############################################################
    ######## Method 2: returns a list[] of hex numbers #########
    size = 0
    hex_values = []
    for c in s:
        #hex_value = "{:02X}".format(ord(c)) # ord(c) converts a character 'c' to its corresponding ASCII/Unicode integer value
        hex_value = ord(c)
        hex_values.append(hex_value)
        size += 1
    return hex_values, size
    #return ' '.join(hex_values)
    ############################################################

def hex_to_string(hex_string):
    # Convert hex string to bytes
    bytes_data = bytes.fromhex(hex_string)
    # Decode bytes to string
    original_string = bytes_data.decode('ascii')
    return original_string

uart0 = UART(0, baudrate=9600, parity=None, stop=1, bits=8, tx=Pin(0), rx=Pin(1), timeout=10) # the serial pins for USB
uart1 = UART(1, baudrate=9600, parity=None, stop=1, bits=8, tx=Pin(4), rx=Pin(5), timeout=10) # the serial pins for UART1
english_message = "hello"
byte_data = english_message.encode('ascii')
print(byte_data)
hexPayload, payload_length = string_to_hex(english_message)
print(f"payload_length = {payload_length}")
frame = add_ending(add_header(hexPayload))
print(english_message, frame)
#hex_string = ''.join(frame)
#uart1.write(bytes([0xAA, 0xAA, 0x20, 0x55]))
uart1.write(bytes(frame))
#english_message = hex_to_string(hex_string)
#uart1.write(english_message)
time.sleep(0.1) # wait

payload = bytes()
payloadBytesReceived = 0
payloadReceived = False
endingBitReceived = False
lookingForHeader = True
lookingForPayload = False
while uart0.any() > 0:
    bytesOnLine = uart0.any()
    #r = uart0.read(1)
    print(f"uart0 contains: {bytesOnLine}")
    #print(f"byte received = {r}")
    if lookingForPayload:
        payload += uart0.read(1)
        payloadBytesReceived += 1
        print(f"payload = {payload}")
        print(f"payloadBytesReceived = {payloadBytesReceived}")
        if payloadBytesReceived > payload_length:
            payloadReceived = True
            lookingForPayload = False
            print(f"payloadReceived = {payloadReceived}")
            continue
    if lookingForHeader:
        if uart0.read(1) == b'\xaa':
            headers_seen += 1
            print(f"headers_seen = {headers_seen}")
            if headers_seen == 3:
                lookingForHeader = False
                lookingForPayload = True
                continue
    if payloadReceived:
        if uart0.read(1) == b'\xaa':
            endingBitReceived = True
            print(f"Frame received. Payload was: {payload}")
        else:
            print(f"Ending byte not received. Payload was: {payload}")
    else:
        lookingForHeader = True
        continue
    

# rxData = bytes() # creates an empty bytes object 
# rxData += uart0.read()
# print(rxData)