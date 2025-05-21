from flask import Flask, render_template, request
import motors.stepper as stepper
import threading

app = Flask(__name__)
current_direction = None
control_lock = threading.Lock()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/mover", methods=["POST"])
def mover():
    global current_direction
    
    direccion = request.form.get("direccion")
    
    with control_lock:
        current_direction = direccion
        
        if direccion == "adelante":
            stepper.move_forward()
        elif direccion == "atras":
            stepper.move_backward()
        elif direccion == "izquierda":
            stepper.move_left()
        elif direccion == "derecha":
            stepper.move_right()
        elif direccion == "parar":
            stepper.stop_motor()
    
    return "OK", 200

def get_current_direction():
    with control_lock:
        return current_direction