import sys
import ingescape as igs
import pygetwindow as pgw 

NAME = "WhiteboardPosition"

def service_callback(sender_agent_name, sender_agent_uuid, service_name, arguments, token, my_data):
    if service_name == "getWhiteboardInfo":
        window = pgw.getWindowsWithTitle("Whiteboard")
        if window:
            igs.service_call(sender_agent_uuid, "receiveWhiteboardInfo", ("ok"), "")
            #return({"x":window[0].left, "y":window[0].top, "width":window[0].width, "height":window[0].height})

if __name__ == "__main__":
    ### AGENT DEFINITION
    # Name
    igs.agent_set_name(NAME)
    # Inputs
    None
    # Outputs
    None
    # Services
    igs.service_init("getWhiteboardInfo", service_callback, None)
    # Connection
    igs.start_with_device("Loopback Pseudo-Interface 1", 5670)

    print(NAME)

    input()

    igs.stop()

