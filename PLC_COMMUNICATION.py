import snap7
import struct
client = snap7.client.Client()
client.connect("192.168.10.10", 0, 1)
client.get_connected()
if client.get_connected():
    print("CONNECTED")

try:
    reading = client.db_read(1, 0, 32)
    a = snap7.util.get_real(reading,2)
    b = snap7.util.get_real(reading,6)
    c = snap7.util.get_real(reading,10)
    d = snap7.util.get_real(reading, 14)
    e = snap7.util.get_real(reading, 18)

    print(a)
    print(b)
    print(c)
    print(d)
    print(e)

    reading1 = client.db_read(1, 0, 32)
    int1 = snap7.util.get_int(reading1,22)
    int2 = snap7.util.get_int(reading1, 24)
    int3 = snap7.util.get_int(reading1, 26)
    int4 = snap7.util.get_int(reading1, 28)
    int5 = snap7.util.get_int(reading1, 30)

    print(int1)
    print(int2)
    print(int3)
    print(int4)
    print(int5)

    reading2 = client.db_read(1, 0, 32)
    bool1 = snap7.util.get_bool(reading2,0,0)
    bool2 = snap7.util.get_bool(reading2,0,1)
    bool3 = snap7.util.get_bool(reading2,0,2)
    bool4 = snap7.util.get_bool(reading2,0,3)
    bool5 = snap7.util.get_bool(reading2,0,4)

    print(bool1)
    print(bool2)
    print(bool3)
    print(bool4)
    print(bool5)

    # a = snap7.util.get_bool(reading, 0, 4)
    # print(a)
    print("Read successful")
except Exception as e:
    print(f"Error reading from PLC: {e}")
