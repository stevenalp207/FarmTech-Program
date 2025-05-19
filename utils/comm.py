import serial
import time
import struct

class SerialComm:
    def __init__(self, port='/dev/ttyUSB0', baudrate=9600, timeout=1):
        self.ser = serial.Serial(port, baudrate, timeout=timeout)

    def send_data(self, data: bytes):
        """Envía datos en bytes por el puerto serial."""
        self.ser.write(data)

    def read_data(self, size=64):
        """Lee una cantidad de bytes del puerto serial."""
        return self.ser.read(size)

    def send_packet(self, payload: bytes):
        """Envía un paquete con encabezado y checksum simple."""
        header = b'\xAA\xBB'
        checksum = sum(payload) % 256
        packet = header + payload + bytes([checksum])
        self.send_data(packet)

    def read_packet(self):
        """Lee un paquete con encabezado y verifica el checksum."""
        data = self.read_data(128)
        if b'\xAA\xBB' in data:
            idx = data.find(b'\xAA\xBB')
            payload = data[idx+2:-1]
            checksum = data[-1]
            if sum(payload) % 256 == checksum:
                return payload
        return None

    def close(self):
        self.ser.close()
