import os, json, socket, sys, threading, io, datetime
from inspect import getframeinfo, stack

with open(("/home/csimon/q37/epeios/tools/ucuq/frontend/wrappers/PYH/" if "Q37_EPEIOS" in os.environ else "../") + "ucuq.json", "r") as config:
  CONFIG = json.load(config)

SELECTOR = CONFIG["Selector"]

UCUQ_DEFAULT_HOST_ = "ucuq.q37.info"
UCUQ_DEFAULT_PORT_ = "53800"

UCUQ_HOST_ = CONFIG["Proxy"]["Host"] if "Proxy" in CONFIG and "Host" in CONFIG["Proxy"] and CONFIG["Proxy"]["Host"] else UCUQ_DEFAULT_HOST_
UCUQ_PORT_ = CONFIG["Proxy"]["Port"] if "Proxy" in CONFIG and "Port" in CONFIG["Proxy"] and CONFIG["Proxy"]["Port"] else UCUQ_DEFAULT_PORT_

PROTOCOL_LABEL_ = "c37cc83e-079f-448a-9541-5c63ce00d960"
PROTOCOL_VERSION_ = "0"

_writeLock = threading.Lock()

# Request
R_PING_ = "Ping_1"
R_EXECUTE_ = "Execute_1"

# Answer
A_OK_ = 0
A_ERROR_ = 1
A_PUZZLED_ = 2
A_DISCONNECTED = 3

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
    s.connect(socket.getaddrinfo(UCUQ_HOST_, UCUQ_PORT_)[0][-1])
  except:
    exit_("FAILURE!!!")
  else:
    print("\r                                         \r",end="")

  return s
  

def handshake_(socket):
  with _writeLock:
    writeString_(socket, PROTOCOL_LABEL_)
    writeString_(socket, PROTOCOL_VERSION_)
    writeString_(socket, "Frontend")
    writeString_(socket, "PYH")

  error = readString_(socket)

  if error:
    sys.exit(error)

  notification = readString_(socket)

  if notification:
    pass
    # print(notification)


def getTokenAndId_(alias):
  return SELECTOR[0], SELECTOR[1][alias]


def ignition_(socket, alias):
  token, id = getTokenAndId_(alias)

  writeString_(socket, token)
  writeString_(socket, id)

  error = readString_(socket)

  if error:
    raise Error(error)


def connect(alias):
  socket = init_()
  handshake_(socket)
  ignition_(socket, alias)

  return socket


class Error(Exception):
  pass


class UCUq:
  def connect_(self, alias):
    self.socket_ = connect(alias)


  def __init__(self, alias=None):
    self.socket_ = connect(alias) if alias else None


  def connect(self, alias):
    try:
      self.connect_(alias)
    except:
      return False
    else:
      return True


  def execute(self, script, expression = ""):
    if self.socket_:
      writeString_(self.socket_, R_EXECUTE_)
      writeString_(self.socket_, script)
      writeString_(self.socket_, expression)

      if ( answer := readUInt_(self.socket_) ) == A_OK_:
        if result := readString_(self.socket_):
          with io.StringIO(result) as stream:
            returned = json.load(stream)
          return returned
        else:
          return None
      elif answer == A_ERROR_:
        result = readString_(self.socket_)
        print(f"\n>>>>>>>>>> ERROR FROM BACKEND BEGIN <<<<<<<<<<")
        print("Timestamp: ", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') )
        caller = getframeinfo(stack()[1][0])
        print(f"Caller: {caller.filename}:{caller.lineno}")
        print(f">>>>>>>>>> ERROR FROM BACKEND CONTENT <<<<<<<<<<")
        print(result)
        print(f">>>>>>>>>> END ERROR FROM BACKEND END <<<<<<<<<<")
      elif answer == A_PUZZLED_:
        readString_(self.socket_) # For future use
        raise Error("Puzzled!")
      elif answer == A_DISCONNECTED:
          raise Error("Disconnected from backend!")
      else:
        raise Error("Unknown answer from backend!")
      
    def ping(self):
      writeString_(self.socket_, R_PING_)

      if ( answer := readUInt_(self.socket_) ) == A_OK_:
        readString_(self.socket_) # For future use
        pass
      elif answer == A_ERROR_:
        raise Error("Unexpected response from backend!")
      elif answer == A_PUZZLED_:
        readString_(self.socket_) # For future use
        raise Error("Puzzled!")
      elif answer == A_DISCONNECTED:
          raise Error("Disconnected from backend!")
      else:
        raise Error("Unknown answer from backend!")

    
