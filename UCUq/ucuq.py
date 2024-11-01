import os, json, socket, sys, threading, datetime
from inspect import getframeinfo, stack

CONFIG_FILE = ( "/home/csimon/q37/epeios/tools/ucuq/remote/wrappers/PYH/" if "Q37_EPEIOS" in os.environ else "../" ) + "ucuq.json"

if not os.path.isfile(CONFIG_FILE):
  print("Please launch the 'Config' app first to set the device to use!")
  sys.exit(0)

with open(CONFIG_FILE, "r") as config:
  CONFIG_ = json.load(config)

DEVICE_ = CONFIG_["Device"]

UCUQ_DEFAULT_HOST_ = "ucuq.q37.info"
UCUQ_DEFAULT_PORT_ = "53800"

UCUQ_HOST_ = CONFIG_["Proxy"]["Host"] if "Proxy" in CONFIG_ and "Host" in CONFIG_["Proxy"] and CONFIG_["Proxy"]["Host"] else UCUQ_DEFAULT_HOST_

# only way to test if the entry contains a valid int.
try:
  UCUQ_PORT_ = int(CONFIG_["Proxy"]["Port"])
except:
  UCUQ_PORT_ = int(UCUQ_DEFAULT_PORT_)

PROTOCOL_LABEL_ = "c37cc83e-079f-448a-9541-5c63ce00d960"
PROTOCOL_VERSION_ = "0"

_writeLock = threading.Lock()
uuid_ = 0

ITEMS_ = "i_"

# Request
R_PING_ = "Ping_1"
R_EXECUTE_ = "Execute_1"
R_UPLOAD_ = "Upload_1"

# Answer
A_OK_ = 0
A_ERROR_ = 1
A_PUZZLED_ = 2
A_DISCONNECTED = 3

def GetUUID_():
  global uuid_

  uuid_ += 1

  return uuid_

def recv_(socket, size):
  buffer = bytes()
  l = 0

  while l != size:
    buffer += socket.recv(size-l)
    l = len(buffer)

  return buffer


def send_(socket, value):
  totalAmount = len(value)
  amountSent = 0

  while amountSent < totalAmount:
    amountSent += socket.send(value[amountSent:])


def writeUInt_(socket, value):
  result = bytes([value & 0x7f])
  value >>= 7

  while value != 0:
    result = bytes([(value & 0x7f) | 0x80]) + result
    value >>= 7

  send_(socket, result)


def writeString_(socket, string):
  bString = bytes(string, "utf-8")
  writeUInt_(socket, len(bString))
  send_(socket, bString)


def writeStrings_(socket, strings):
  writeUInt_(socket, len(strings))

  for string in strings:
    writeString_(socket, string)


def readByte_(socket):
  return ord(recv_(socket, 1))


def readUInt_(socket):
  byte = readByte_(socket)
  value = byte & 0x7f

  while byte & 0x80:
    byte = readByte_(socket)
    value = (value << 7) + (byte & 0x7f)

  return value


def readString_(socket):
  size = readUInt_(socket)

  if size:
    return recv_(socket, size).decode("utf-8")
  else:
    return ""


def exit_(message=None):
  if message:
    print(message, file=sys.stderr)
  sys.exit(-1)


def init_():
  s = socket.socket()

  print("Connection to UCUq server…", end="", flush=True)

  try:
    s.connect((UCUQ_HOST_, UCUQ_PORT_))
  except Exception as e:
    raise e
  else:
    print("\r                                         \r",end="")

  return s


def handshake_(socket):
  with _writeLock:
    writeString_(socket, PROTOCOL_LABEL_)
    writeString_(socket, PROTOCOL_VERSION_)
    writeString_(socket, "Remote")
    writeString_(socket, "PYH")

  error = readString_(socket)

  if error:
    sys.exit(error)

  notification = readString_(socket)

  if notification:
    pass
    # print(notification)


def getTokenAndId_(deviceId):
  return DEVICE_["Token"], DEVICE_["Id"] if deviceId == "" else deviceId


def ignition_(socket, token, deviceId):
  writeString_(socket, token)
  writeString_(socket, deviceId)

  error = readString_(socket)

  if error:
    raise Error(error)


def connect_(token, deviceId):
  socket = init_()
  handshake_(socket)
  ignition_(socket, token, deviceId)

  return socket


class Error(Exception):
  pass


class UCUq_:
  def connect_(self, deviceId):
    self.token, self.deviceId = getTokenAndId_(deviceId)
    self.socket_ = connect_(self.token, self.deviceId)


  def __init__(self, deviceId = None, dryRun=False):
    if ( deviceId != None ) and not dryRun:
      self.connect_(deviceId)

    self.dryRun_ = dryRun


  def __del__(self):
    self.render()


  def connect(self, deviceId = None):
    if not self.dryRun_:
      try:
        self.connect_(deviceId if deviceId != None else "")
      except:
        self.dryRun_ = True
        return False
      else:
        return True


  def getTokenAndDeviceId(self):
    return self.token, self.deviceId


  def getToken(self):
    return self.getTokenAndDeviceId()[0]


  def getDeviceId(self):
    return self.getTokenAndDeviceId()[1]


  def upload(self, modules):
    if self.dryRun_:
      print(modules)
    else:
      writeString_(self.socket_, R_UPLOAD_)
      writeStrings_(self.socket_, modules)

      if ( answer := readUInt_(self.socket_) ) == A_OK_:
        pass
      elif answer == A_ERROR_:
        result = readString_(self.socket_)
        print(f"\n>>>>>>>>>> ERROR FROM DEVICE BEGIN <<<<<<<<<<")
        print("Timestamp: ", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') )
        caller = getframeinfo(stack()[1][0])
        print(f"Caller: {caller.filename}:{caller.lineno}")
        print(f">>>>>>>>>> ERROR FROM DEVICE CONTENT <<<<<<<<<<")
        print(result)
        print(f">>>>>>>>>> END ERROR FROM DEVICE END <<<<<<<<<<")
        sys.exit(0)
      elif answer == A_PUZZLED_:
        readString_(self.socket_) # For future use
        raise Error("Puzzled!")
      elif answer == A_DISCONNECTED:
          raise Error("Disconnected from DEVICE!")
      else:
        raise Error("Unknown answer from device!")


  def execute(self, script, expression = ""):
    if self.dryRun_:
      print(script)
    elif self.socket_:
      writeString_(self.socket_, R_EXECUTE_)
      writeString_(self.socket_, script)
      writeString_(self.socket_, expression)

      if ( answer := readUInt_(self.socket_) ) == A_OK_:
        if result := readString_(self.socket_):
          return json.loads(result)
        else:
          return None
      elif answer == A_ERROR_:
        result = readString_(self.socket_)
        print(f"\n>>>>>>>>>> ERROR FROM DEVICE BEGIN <<<<<<<<<<")
        print("Timestamp: ", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') )
        caller = getframeinfo(stack()[1][0])
        print(f"Caller: {caller.filename}:{caller.lineno}")
        print(f">>>>>>>>>> ERROR FROM DEVICE CONTENT <<<<<<<<<<")
        print(result)
        print(f">>>>>>>>>> END ERROR FROM DEVICE END <<<<<<<<<<")
        sys.exit(0)
      elif answer == A_PUZZLED_:
        readString_(self.socket_) # For future use
        raise Error("Puzzled!")
      elif answer == A_DISCONNECTED:
          raise Error("Disconnected from DEVICE!")
      else:
        raise Error("Unknown answer from device!")


  def ping(self):
    writeString_(self.socket_, R_PING_)

    if ( answer := readUInt_(self.socket_) ) == A_OK_:
      readString_(self.socket_) # For future use
    elif answer == A_ERROR_:
      raise Error("Unexpected response from device!")
    elif answer == A_PUZZLED_:
      readString_(self.socket_) # For future use
      raise Error("Puzzled!")
    elif answer == A_DISCONNECTED:
        raise Error("Disconnected from device!")
    else:
      raise Error("Unknown answer from device!")
    
    
class UCUq(UCUq_):
  def __init__(self, deviceId = None, dryRun = False):
    super().__init__(deviceId, dryRun)
    self.pendingModules = ["Init"]
    self.handledModules = []
    self.commands = []


  def connect(self, deviceId = None):
    super().connect(deviceId)


  def addModule(self, module):
    if not module in self.pendingModules and not module in self.handledModules:
      self.pendingModules.append(module)


  def addCommand(self, command):
    self.commands.append(command)


  def render(self, expression = ""):
    result = ""

    if self.pendingModules:
      super().upload(self.pendingModules)
      self.handledModules.extend(self.pendingModules)
      self.pendingModules = []

    if self.commands:
      result = super().execute('\n'.join(self.commands), expression)
      self.commands = []

    return result


  def servoMoves(self, moves, speed = 1):
    self.addModule("ServoMoves")

    command = "servoMoves([\n"

    for move in moves:
      servo = move[0]

      step = speed * (servo.specs.max - servo.specs.min) / servo.specs.range

      command += f"\t[{move[0].pwm.getObject()},{move[0].angleToDuty(move[1])}],\n"

    command += f"], {int(step)})"

    self.addCommand(command)



class Core_:
  def __init__(self, ucuq, module = ""):
    self.ucuq = ucuq
    if module:
      self.ucuq.addModule(module)
    self.id = None

  
  def __del__(self):
    if self.id:
      self.addCommand(f"del {ITEMS_}[{self.id}]")

  
  def init(self):
    self.id = GetUUID_()

  
  def execute(self, script, expr = ""):
    return self.ucuq.execute(script, expr)
    
    
  def getObject(self):
    return f"{ITEMS_}[{self.id}]"
  
  
  def addCommand(self, command):
    self.ucuq.addCommand(command)
                         
                         
  def render(self):
    self.ucuq.render()
  

class GPIO(Core_):
  def __init__(self, ucuq, pin = None):
    super().__init__(ucuq, "GPIO")

    if pin:
      self.init(pin)


  def init(self, pin):
    super().init()
    self.pin = f'"{pin}"' if isinstance(pin,str) else pin

    self.addCommand(f"{self.getObject()} = GPIO({self.pin})")


  def on(self, state = True):
    self.addCommand(f"{self.getObject()}.on({state})")


  def off(self):
    self.on(False)


class HT16K33(Core_):
  def __init__(self, ucuq, sda = None, scl = None):
    super().__init__(ucuq, "HT16K33")

    if bool(sda) != bool(scl):
      raise Exception("None or both of sda/scl must be defined!")
    elif sda:
      self.init(sda, scl)


  def init(self, sda, scl):
    super().init()

    self.ucuq.addCommand(f"{self.getObject()} = HT16K33(machine.I2C(0, sda=machine.Pin({sda}), scl=machine.Pin({scl})))")
    self.ucuq.addCommand(f"{self.getObject()}.set_brightness(0)")


  def setBlinkRate(self, rate):
    self.execute(f"{self.getObject()}.set_blink_rate({rate})")

  def setBrightness(self, brightness):
    self.execute(f"{self.getObject()}.set_brightness({brightness})")

  def clear(self):
    self.ucuq.addCommand(f"{self.getObject()}.clear()")
    self.render()

  def plot(self, x, y):
    self.ucuq.addCommand(f"{self.getObject()}.plot({x},{y})")

  def draw(self, motif):
    self.ucuq.addCommand(f"{self.getObject()}.clear().draw('{motif}').render()")
    self.render()

  def render(self):
    self.ucuq.addCommand(f"{self.getObject()}.render()")
    super().render()



class PCA9685(Core_):
  def __init__(self, ucuq, sda = None, scl = None, freq = None, addr = None):
    super().__init__(ucuq, "PCA9685")

    if (sda != None) != bool(scl != None) :
      raise Exception("None or both of 'sda'/'scl' must be defined!")
    
    if sda:
      self.init(sda, scl, freq = freq, addr = addr)
    elif freq:
      raise Exception("'freq' cannot be defined without 'sda' and 'scl'!")
    elif addr:
      raise Exception("'addr' cannot be defined without 'sda' and 'scl'!")


  def init(self, sda, scl, *, freq = None, addr = None):
    super().init()

    self.addCommand(f"{self.getObject()} = PCA9685({sda}, {scl}, {addr if addr else 0x40})")
    self.freq(freq if freq else 50)


  def deinit(self):
    self.addCommand(f"{self.getObject()}.reset()")
                    

  def nsToU12_(self, duty_ns):
    return int(self.freq() * duty_ns * 0.000004095)
  
  def u12ToNS_(self, value):
    return int(200000000 * value / (self.freq() * 819))
  

  def freq(self, freq = None):
    if freq:
      self.addCommand(f"{self.getObject()}.freq({freq if freq else 50})")
    else:
      return self.execute("", f"{self.getObject()}.freq()")
  

class PCA9685Channel(Core_):
  def __init__(self, ucuq, pca = None, channel = None, /):
    super().__init__(ucuq, "PCA9685Channel")

    if bool(pca) != (channel != None):
      raise Exception("Both or none of 'pca' and 'channel' must be defined!")
    
    if pca:
      self.init(pca, channel)


  def init(self, pca, channel):
    super().init()

    self.pca = pca # Not used inside this object, but to avoid pca being destroyed by GC, as it is used on the µc.
    self.addCommand(f"{self.getObject()} = PCA9685Channel({pca.getObject()}, {channel})")

  def deinit(self):
    self.addCommand(f"{self.getObject()}.deinit()")


  def duty_ns(self, ns = None):
    if ns == None:
      return int(self.execute("", f"{self.getObject()}.duty_ns()"))
    self.addCommand(f"{self.getObject()}.duty_ns({ns})")


  def duty_u16(self, u16 = None):
    if u16 == None:
      return int(self.execute("",f"{self.getObject()}.duty_u16()"))
    self.addCommand(f"{self.getObject()}.duty_u16({u16})")
  

  def freq(self, freq = None):
    if freq == None:
      return int(self.execute("",f"{self.getObject()}.freq()"))
    self.addCommand(f"{self.getObject()}.freq({freq})")
  

class PWM(Core_):
  def __init__(self, ucuq, pin = None, freq = None):
    super().__init__(ucuq, "PWM")

    if freq != None:
      if pin == None:
        raise Exception("'freq' cannot be defined without 'pin'!")
      
    if pin != None:
      self.init(pin, freq)


  def init(self, pin, freq = None):
    super().init()

    self.addCommand(f"{self.getObject()} = machine.PWM(machine.Pin({pin}),freq={freq if freq else 50})")


  def duty_u16(self, u16 = None):
    if u16 == None:
      return int(self.execute("", f"{self.getObject()}.duty_u16()"))
    self.addCommand(f"{self.getObject()}.duty_u16({u16})")


  def duty_ns(self, ns = None):
    if ns == None:
      return int(self.execute("", f"{self.getObject()}.duty_ns()"))
    self.addCommand(f"{self.getObject()}.duty_ns({ns})")


  def freq(self, freq = None):
    if freq == None:
      return int(self.execute("", f"{self.getObject()}.freq()"))
    self.addCommand(f"{self.getObject()}.freq({freq})")


  def deinit(self):
    self.addCommand(f"{self.getObject()}.deinit()")



class Servo(Core_):
  class Specs:
    def __init__(self, u16_min, u16_max, range):
      self.min = u16_min
      self.max = u16_max
      self.range = range
  
  class Tweak:
    def __init__(self, angle, u16_offset, invert):
      self.angle = angle
      self.offset = u16_offset
      self.invert = invert
  
  class Domain:
    def __init__(self, u16_min, u16_max):
      self.min = u16_min
      self.max = u16_max


  def test_(self, pwm, specs, tweak, domain):
    if tweak:
      if not specs:
        raise Exception("'tweak' can not be defined without 'specs'!")

    if domain:
      if not specs:
        raise Exception("'domain' can not be defined without 'specs'!")


  def __init__(self, ucuq, pwm = None, specs = None, /, *, tweak = None, domain = None):
    super().__init__(ucuq, "Servo")

    self.test_(pwm, specs, tweak, domain)

    if pwm:
      self.init(pwm, specs, tweak = tweak, domain = domain)


  def init(self, pwm, specs, tweak = None, domain = None):
    super().init()

    self.test_(pwm, specs, tweak, domain)

    if not tweak:
      tweak = self.Tweak(specs.range/2, 0, False)

    if not domain:
      domain = self.Domain(specs.min, specs.max)

    self.specs = specs
    self.tweak = tweak
    self.domain = domain

    self.pwm = pwm

    self.reset()


  def angleToDuty(self, angle):
    if self.tweak.invert:
      angle = -angle

    u16 = self.specs.min + ( angle + self.tweak.angle ) * ( self.specs.max - self.specs.min ) / self.specs.range + self.tweak.offset

    if u16 > self.domain.max:
      u16 = self.domain.max
    elif u16 < self.domain.min:
      u16 = self.domain.min

    return int(u16)
  

  def dutyToAngle(self, duty):
    angle = self.specs.range * ( duty - self.tweak.offset - self.specs.min ) / ( self.specs.mas - self.specs.min )

    if self.tweak.invert:
      angle = -angle

    return angle - self.tweak.angle


  def reset(self):
    self.angle(0)


  def angle(self, angle = None):
    if angle == None:
      return self.dutyToAngle(self.pwm.duty_u16())
    else:
      self.pwm.duty_u16(self.angleToDuty(angle))


class WS2812(Core_):
  def __init__(self, ucuq, pin = None, n = None):
    super().__init__(ucuq, "WS2812")

    if (pin == None) != (n == None):
      raise Exception("Both or none of 'pin'/'n' must be defined")

    if pin != None:
      self.init(pin, n)

  def init(self, pin, n):
    super().init()

    self.addCommand(f"{self.getObject()} = neopixel.NeoPixel(machine.Pin({pin}), {n})")


  def len(self):
    return int(self.execute("", f"{self.getObject()}.__len__()"))
               

  def value(self, index, val = None):
    if val == None:
      return self.execute("", f"{self.getObject()}.__getitem__({index})")
    self.addCommand(f"{self.getObject()}.setitem({index}, {json.dumps(val)})")
                       
  def fill(self, val):
    print("Val: ", val)
    self.addCommand(f"{self.getObject()}.fill({json.dumps(val)})")

  def write(self):
    self.addCommand(f"{self.getObject()}.write()")
    self.render()
    
  


    