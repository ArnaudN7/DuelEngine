from time import sleep
import ingescape as igs

# ONLY MODIFY ELEMENTS THAT ARE IDENTIFIED WITH #MODIFYIT!
# You can CTRL+F #MODIFYIT! to make it easier

NAME = "YOURGAMENAME" #MODIFYIT!
RULES = "YOURRULES" #MODIFYIT!
BOARD = "A png url of your board in such dimensions as : <<CASE_LENGTH*BOARD_COL>>x<<CASE_HEIGHT*BOARD_ROW>>" #MODIFYIT!
GAME_IMAGE = "A png url of your game in 300x300" #MODIFYIT!
CASE_LENGTH = 200 #MODIFYIT!
CASE_HEIGHT = 200 #MODIFYIT!
BOARD_COL = 3 #MODIFYIT!
BOARD_ROW = 3 #MODIFYIT!

# Input callback
def input_callback(iop_type, name, value_type, value, my_data):
    if name == "action":
        if igs.input_string("currentGame") == NAME:
            game_action(igs.input_int("x"), igs.input_int("y"))
    if name == "reset":
        if igs.input_string("currentGame") == NAME:
            game_reset()

def on_agent_event_callback(event, uuid, name, event_data, my_data):
   if event == igs.AGENT_KNOWS_US and name == "DuelEngine":
        register()

def agent_init():
    ### AGENT DEFINITION
    # Name
    igs.agent_set_name(NAME)
    igs.definition_set_version("1.0")
    igs.definition_set_description("""A short description of your game""") #MODIFYIT!
    # Inputs
    igs.input_create("currentGame", igs.STRING_T, None)
    igs.input_create("x", igs.INTEGER_T, None)
    igs.input_create("y", igs.INTEGER_T, None)
    igs.input_create("action", igs.IMPULSION_T, None)
    igs.input_create("reset", igs.IMPULSION_T, None)
    # Inputs callback
    igs.observe_input("currentGame", input_callback, None)
    igs.observe_input("x", input_callback, None)
    igs.observe_input("y", input_callback, None)
    igs.observe_input("action", input_callback, None)
    igs.observe_input("reset", input_callback, None)
    # Outputs
    igs.output_create("player1_win", igs.IMPULSION_T, None)
    igs.output_create("player2_win", igs.IMPULSION_T, None)
    igs.output_create("tie", igs.IMPULSION_T, None)
    igs.output_create("player1_turn", igs.IMPULSION_T, None)
    igs.output_create("player2_turn", igs.IMPULSION_T, None)
    # Services
    None
    # Observe agent
    igs.observe_agent_events(on_agent_event_callback, None)
    # Connection
    igs.start_with_device("Loopback Pseudo-Interface 1", 5670)

def init():
    agent_init()

def register():
    igs.mapping_add("currentGame", "DuelEngine", "currentGame")
    igs.mapping_add("x", "DuelEngine", "x")
    igs.mapping_add("y", "DuelEngine", "y")
    igs.mapping_add("action", "DuelEngine", "gameAction")
    igs.mapping_add("reset", "DuelEngine", "gameReset")
    arguments = (NAME, RULES, BOARD, GAME_IMAGE, CASE_LENGTH, CASE_HEIGHT, BOARD_COL, BOARD_ROW)
    igs.service_call("DuelEngine", "gameRegister", arguments, "")
        
def unregister():
    igs.service_call("DuelEngine", "gameUnregister", (), "")
    igs.mapping_remove_with_name("currentGame", "DuelEngine", "currentGame")
    igs.mapping_remove_with_name("x", "DuelEngine", "x")
    igs.mapping_remove_with_name("y", "DuelEngine", "y")
    igs.mapping_remove_with_name("action", "DuelEngine", "gameAction")
    igs.mapping_remove_with_name("reset", "DuelEngine", "gameReset")

### GLOBAL VARIABLES
player1_started_last_game = False
player1_turn = True
game_memory = [] #MODIFYIT!
### --- GLOBAL VARIABLES

### FUNCTIONS : WITH A IGS CALL

def player_turn():
    next_turn = "player1_turn" if player1_turn else "player2_turn"
    igs.output_set_impulsion(next_turn)

def player_win():
    winner = "player1_win" if player1_turn else "player2_win"
    igs.output_set_impulsion(winner)

def tie():
    igs.output_set_impulsion("tie")
    
### --- FUNCTIONS : WITH A IGS CALL
    
### FUNCTIONS : CALLBACK OF INPUTS
    
def game_action(x : int, y : int):
    win, switch = action_result(x, y)
    if win:
        player_win()
    else:
        if switch:
            switch_player_turn()
            player_turn()

def game_reset(): #MODIFYIT!
    global player1_turn
    global player1_started_last_game
    ###
    global game_memory
    game_memory = []
    ###
    player1_turn = not player1_started_last_game
    player1_started_last_game = not player1_started_last_game
    player_turn()

### --- FUNCTIONS : CALLBACK OF INPUTS

### FUNCTIONS : CORE PROGRAM
    
def switch_player_turn():
    global player1_turn
    player1_turn = not player1_turn

def win_condition(): #MODIFYIT!
    return True

def tie_condition(): #MODIFYIT!
    return True 

def action_result(x : int, y : int): #MODIFYIT!
    win = False
    switch = False
    if x != 0 and y != 0: # If in board
        # Any code here if actions may occur such as adding graphical stuff
        if win_condition():
            switch = False
            win = True
        else:
            if tie_condition():
                switch = False
                tie()
    return win, switch

### --- FUNCTIONS : CORE PROGRAM

init()

print(NAME)

input()

unregister()

sleep(1) # Ensure unregister

igs.stop()