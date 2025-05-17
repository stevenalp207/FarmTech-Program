# motors/stepper.py
import time
import board
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper

# Inicializar el MotorKit (motor paso a paso)
kit = MotorKit(i2c=board.I2C())

def move_stepper_motor_continuous(delay=0.001):
    """
    Mueve ambos motores paso a paso continuamente en la dirección hacia adelante.
    
    :param delay: Tiempo en segundos de espera entre cada paso. (menor delay = mayor velocidad)
    """
    while True:  # Bucle infinito para mover los motores sin detenerse
        kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
        kit.stepper2.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
        time.sleep(delay)

def stop_motor():

    kit.stepper1.release()
    kit.stepper2.release()
    print("Motores detenidos.")
