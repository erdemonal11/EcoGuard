# scd4x.py — MicroPython driver for Sensirion SCD4x sensors (SCD40/SCD41)

import time
import struct

class SCD4X:
    def __init__(self, i2c, addr=0x62):
        self.i2c = i2c
        self.addr = addr
        self._buf = bytearray(9)

    def _write_cmd(self, cmd):
        self.i2c.writeto(self.addr, struct.pack(">H", cmd))

    def _read_words(self, cmd, n):
        self._write_cmd(cmd)
        time.sleep_ms(1)
        data = self.i2c.readfrom(self.addr, n * 3)
        result = []
        for i in range(n):
            word = data[i * 3] << 8 | data[i * 3 + 1]
            result.append(word)
        return result

    def start_periodic_measurement(self):
        self._write_cmd(0x21B1)

    def stop_periodic_measurement(self):
        self._write_cmd(0x3F86)
        time.sleep_ms(500)

    @property
    def data_ready(self):
        ready = self._read_words(0xE4B8, 1)[0]
        return ready & 0x07FF

    @property
    def measurement(self):
        raw = self._read_words(0xEC05, 3)
        co2 = raw[0]
        temperature = -45 + 175 * (raw[1] / 65535.0)
        humidity = 100 * (raw[2] / 65535.0)
        return co2, temperature, humidity

