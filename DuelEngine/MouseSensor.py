from pynput import mouse
import ingescape as igs

NAME = "MouseSensor"

def agent_init():
    ### AGENT DEFINITION
    # Name
    igs.agent_set_name(NAME)
    # Inputs
    None
    # Outputs
    igs.output_create("mouse_x", igs.INTEGER_T, None)
    igs.output_create("mouse_y", igs.INTEGER_T, None)
    igs.output_create("click", igs.IMPULSION_T, None)
    # Services
    None
    # Connection
    igs.start_with_device("Loopback Pseudo-Interface 1", 5670)

def init():
    agent_init()
    
def on_move(x,y):
    igs.output_set_int("mouse_x", x)
    igs.output_set_int("mouse_y", y)

def on_click(x, y, button, pressed):
    if(pressed):
        igs.output_set_int("mouse_x", x)
        igs.output_set_int("mouse_y", y)
        igs.output_set_impulsion("click")
        

init()

print(NAME)

# Collect events
with mouse.Listener(
        on_move=on_move,
        on_click=on_click) as listener:
    listener.join()

input()

igs.stop()