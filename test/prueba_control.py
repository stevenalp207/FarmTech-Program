import pygame
import time

pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("No se detectó ningún joystick.")
    exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()
print(f"Joystick detectado: {joystick.get_name()}")

try:
    while True:
        pygame.event.pump()

        l1 = joystick.get_axis(2)
        r1 = joystick.get_axis(2)

        l2 = joystick.get_axis(4)
        r2 = joystick.get_axis(5)

        print(f"L2: {l2:.3f} | R2: {r2:.3f} | L1: {l1} | R1: {r1}")

        # Ajusta el umbral de presión según los valores que veas
        l2_pressed = l2 > 0.5
        r2_pressed = r2 > 0.5

        l1_pressed = l1 < -0.8 #izquierda
        r1_pressed = r1 > 0.8 #derecha

        if r2_pressed:
            print("Avanzando (R2 presionado)")
        elif l2_pressed:
            print("Retrocediendo (L2 presionado)")

        if r1_pressed:
            print("Girando a la derecha (R1 presionado)")
        if l1_pressed:
            print("Girando a la izquierda (L1 presionado)")

        time.sleep(0.2)

except KeyboardInterrupt:
    print("Terminando...")

finally:
    pygame.quit()
