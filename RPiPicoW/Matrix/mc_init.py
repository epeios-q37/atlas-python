from machine import I2C, Pin
import time

class Matrix:
  HT16K33_GENERIC_DISPLAY_ON = 0x81
  HT16K33_GENERIC_DISPLAY_OFF = 0x80
  HT16K33_GENERIC_SYSTEM_ON = 0x21
  HT16K33_GENERIC_SYSTEM_OFF = 0x20
  HT16K33_GENERIC_DISPLAY_ADDRESS = 0x00
  HT16K33_GENERIC_CMD_BRIGHTNESS = 0xE0
  HT16K33_GENERIC_CMD_BLINK = 0x81
  width = 16
  height = 8

  def __init__(self, i2c, i2c_address=0x71):
    assert 0x00 <= i2c_address < 0x80, "ERROR - Invalid I2C address in HT16K33()"
    self.buffer = bytearray(self.width * 2)
    self.i2c = i2c
    self.address = i2c_address
    self.power_on()

  def power_on(self):
    self._write_cmd(self.HT16K33_GENERIC_SYSTEM_ON)
    self._write_cmd(self.HT16K33_GENERIC_DISPLAY_ON)

  def power_off(self):
    self._write_cmd(self.HT16K33_GENERIC_DISPLAY_OFF)
    self._write_cmd(self.HT16K33_GENERIC_SYSTEM_OFF)    

  def _write_cmd(self, byte):
    self.i2c.writeto(self.address, bytes([byte]))


  def plot(self, x, y, ink=1, xor=False):
    # Bail on incorrect row numbers or character values
    assert (0 <= x < self.width) and (0 <= y < self.height), "ERROR - Invalid coordinate set in plot()"

    if ink not in (0, 1): ink = 1
    x2 = self._get_row(x)
    if ink == 1:
      if self.is_set(x ,y) and xor:
        self.buffer[x2] ^= (1 << y)
      else:
        if self.buffer[x2] & (1 << y) == 0: self.buffer[x2] |= (1 << y)
    else:
      if not self.is_set(x ,y) and xor:
        self.buffer[x2] ^= (1 << y)
      else:
        if self.buffer[x2] & (1 << y) != 0: self.buffer[x2] &= ~(1 << y)
    return self

  def _get_row(self, x):
    x = self.width - x - 1
    a = 1 + (x << 1)
    if x < 8: a += 15
    if a >= self.width * 2: return False
    return a

  def is_set(self, x, y):
    # Bail on incorrect row numbers or character values
    assert (0 <= x < self.width) and (0 <= y < self.height), "ERROR - Invalid coordinate set in is_set()"

    x = self._get_row(x)
    bit = (self.buffer[x] >> y) & 1
    return True if bit > 0 else False

  def render(self):
    buffer = bytearray(len(self.buffer) + 1)
    buffer[1:] = self.buffer
    buffer[0] = 0x00
    self.i2c.writeto(self.address, bytes(buffer))

  def set_brightness(self, brightness=15):
    if brightness < 0 or brightness > 15: brightness = 15
    self.brightness = brightness
    self._write_cmd(self.HT16K33_GENERIC_CMD_BRIGHTNESS | brightness)

  def set_blink_rate(self, rate=0):
    allowed_rates = (0, 2, 1, 0.5)
    assert rate in allowed_rates, "ERROR - Invalid blink rate set in set_blink_rate()"
    self.blink_rate = allowed_rates.index(rate) & 0x03
    self._write_cmd(self.HT16K33_GENERIC_CMD_BLINK | self.blink_rate << 1)

  def clear(self):
    for i in range(0, len(self.buffer)): self.buffer[i] = 0x00
    return self
  
  def draw(self, motif):
    for y, c in enumerate(motif):
      for x in range(4):
          if int(c, 16) & (1 << (3 -x)):
            self.plot(x + 4 * (y % 4),7 - (y >> 2))

    return self


i2c = I2C(0, scl=Pin(5), sda=Pin(4))
print(i2c.scan())

matrix = Matrix(i2c)
matrix.set_brightness(0)

def test():
  for y in range(7, -1, -1):
    for x in range(16):
      matrix.plot(x,y)
    matrix.render();
    time.sleep(.06)
    matrix.clear()

  for x in range(16):
    for y in range(8):
      matrix.plot(x,y)
    matrix.render();
    time.sleep(.06)
    matrix.clear()

  for x in range(16):
    for y in range(8):
      matrix.plot(x,y)

  matrix.render()

  for b in range(0, 16):
    matrix.set_brightness(b)
    time.sleep(0.05)

  for b in range(15, -1, -1):
    matrix.set_brightness(b)
    time.sleep(0.05)

  matrix.clear().render()


