import time
import board
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper

# Inicializar el MotorKit (motor paso a paso)
kit = MotorKit(i2c=board.I2C())

def move_forward():
    for i in range(100):
        kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
        kit.stepper2.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
        time.sleep(0.01)

def move_backward():
    for i in range(100):
        kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
        kit.stepper2.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
        time.sleep(0.01)

def move_left():
    for i in range(100):
        kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
        kit.stepper2.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
        time.sleep(0.01)

def move_right():
    for i in range(100):
        kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
        kit.stepper2.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
        time.sleep(0.01)


def stop_motor():
    kit.stepper1.release()
    kit.stepper2.release()
