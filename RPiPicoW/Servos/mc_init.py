# MicroPython code for the µcontroller

from machine import Pin, PWM
import time

class Servo:
  __servo_pwm_freq = 50
  __min_u16_duty = 1640 - 2 # offset for correction
  __max_u16_duty = 7864 - 0  # offset for correction
  min_angle = 0
  max_angle = 180
  current_angle = 0.001


  def __init__(self, pin):
    self.__initialise(pin)


  def update_settings(self, servo_pwm_freq, min_u16_duty, max_u16_duty, min_angle, max_angle, pin):
    self.__servo_pwm_freq = servo_pwm_freq
    self.__min_u16_duty = min_u16_duty
    self.__max_u16_duty = max_u16_duty
    self.min_angle = min_angle
    self.max_angle = max_angle
    self.__initialise(pin)


  def move(self, angle):
    # round to 2 decimal places, so we have a chance of reducing unwanted servo adjustments
    angle = round(angle, 2)
    # do we need to move?
    if angle == self.current_angle:
        return
    self.current_angle = angle
    # calculate the new duty cycle and move the motor
    duty_u16 = self.__angle_to_u16_duty(angle)
    self.__motor.duty_u16(duty_u16)

  def current(self):
    return self.current_angle    

  def __angle_to_u16_duty(self, angle):
    return int((angle - self.min_angle) * self.__angle_conversion_factor) + self.__min_u16_duty


  def __initialise(self, pin):
    self.current_angle = 90.001
    self.__angle_conversion_factor = (self.__max_u16_duty - self.__min_u16_duty) / (self.max_angle - self.min_angle)
    self.__motor = PWM(Pin(pin))
    self.__motor.freq(self.__servo_pwm_freq)


LL_PIN = 10
LF_PIN = 11
RL_PIN = 12
RF_PIN = 13
X1_PIN = 14
X2_PIN = 15

lf = Servo(LF_PIN)
ll = Servo(LL_PIN)
rl = Servo(RL_PIN)
rf = Servo(RF_PIN)
x1 = Servo(X1_PIN)
x2 = Servo(X2_PIN)

servos = {
  "lf": lf,
  "ll": ll,
  "rf": rf,
  "rl": rl,
  "x1": x1,
  "x2": x2
}

def moves_(moves, step):
  if not step:
    for move in moves:
      move[0].move(move[1])
  else:
    step += 1
    cont = True

    while cont:
      cont = False
      for move in moves:
        servo = move[0]
        current = int(servo.current())
        final = move[1]
        if current != final:
          cont = True
          current += 1 if current < final else -1

        servo.move(current)
      for _ in range(step):
        time.sleep(.0025)

def move(rawMoves, step=10):
  moves = []

  for move in rawMoves:
    moves.append((servos[move[0]], move[1]+90))

  moves_(moves, step)
