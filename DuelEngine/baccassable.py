from time import sleep
import ingescape as igs

def agent_init():
    ### AGENT DEFINITION
    # Name
    igs.agent_set_name("NAME")
    # Inputs
    igs.input_create("youhou", igs.STRING_T, None)
    # Connection
    igs.start_with_device("Loopback Pseudo-Interface 1", 5670)

def init():
    agent_init()

def register():
    global id 
    id = igs.mapping_add("youhou", "DuelEngine", "currentGame")
        
def unregister():
    rep = igs.clear_mappings()
    print(rep)

init()

print("NAME")

register()

input()

unregister()

sleep(3) # Ensure call

igs.stop()