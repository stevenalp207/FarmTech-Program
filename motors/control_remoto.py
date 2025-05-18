import pygame
import time

def inicializar_joystick():
    pygame.init()
    pygame.joystick.init()
    if pygame.joystick.get_count() == 0:
        print("No se detectó ningún joystick.")
        return None
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Joystick detectado: {joystick.get_name()}")
    return joystick

def leer_controles(joystick):
    pygame.event.pump()

    l1 = joystick.get_axis(2)
    r1 = joystick.get_axis(2)
    l2 = joystick.get_axis(4)
    r2 = joystick.get_axis(5)

    # Ajusta el umbral para detectar gatillos presionados
    l2_pressed = l2 > 0.5
    r2_pressed = r2 > 0.5
    l1_pressed = l1 < -0.8
    r1_pressed = r1 > 0.8

    return {
        "L2": (l2, l2_pressed),
        "R2": (r2, r2_pressed),
        "L1": (l1, l1_pressed),
        "R1": (r1, r1_pressed)
    }

