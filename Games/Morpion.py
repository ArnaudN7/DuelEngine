#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  ClickIt version 1.0
#  Created by Ingenuity i/o on 2024/01/30
#

from time import sleep
import ingescape as igs

NAME = "Morpion"
BOARD = "https://github.com/ArnaudN7/DuelEngine/blob/main/Games/Images/Morpion_board.png?raw=true"
GAME_IMAGE = "https://github.com/ArnaudN7/DuelEngine/blob/main/Games/Images/Morpion_game_image.png?raw=true"
CASE_LENGTH = 200
BOARD_COL = 3
BOARD_ROW = 3

#inputs
def input_callback(iop_type, name, value_type, value, my_data):
    if name == "action":
        if igs.input_string("currentGame") == NAME:
            game_action(igs.input_int("x"), igs.input_int("y"))
    if name == "reset":
        if igs.input_string("currentGame") == NAME:
            game_reset()
    # add code here if needed

def on_agent_event_callback(event, uuid, name, event_data, my_data):
   if event == igs.AGENT_KNOWS_US and name == "DuelEngine":
        register()

def agent_init():
    ### AGENT DEFINITION
    # Name
    igs.agent_set_name(NAME)
    igs.definition_set_version("1.0")
    igs.definition_set_description("""The classic""")
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
    arguments = (NAME, BOARD, GAME_IMAGE, CASE_LENGTH, CASE_LENGTH, BOARD_COL, BOARD_ROW)
    igs.service_call("DuelEngine", "gameRegister", arguments, "")
        
### GLOBAL VARIABLES
player1_started_last_game = False
player1_turn = True
game_memory = [0,0,0,0,0,0,0,0,0]
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

def add_player_token(x : int, y : int):
    nb = num_case(x, y)
    game_memory[nb] = 1 if player1_turn else 2
    player_color = "PLAYER1COLOR" if player1_turn else "PLAYER2COLOR"
    parameters = ("ellipse", x, y, player_color, "black")
    igs.service_call("DuelEngine", "addShapeInBoard", parameters, "")
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


def game_reset():
    global player1_turn
    global player1_started_last_game
    global game_memory
    game_memory = [0,0,0,0,0,0,0,0,0]
    player1_turn = not player1_started_last_game
    player1_started_last_game = not player1_started_last_game
    player_turn()
### --- FUNCTIONS : CALLBACK OF INPUTS

### FUNCTIONS : CORE PROGRAM
def switch_player_turn():
    global player1_turn
    player1_turn = not player1_turn

def num_case(x : int, y : int):
    return (x + BOARD_COL*(y-1)) - 1

def win_condition():
    first_line = game_memory[0] != 0 and (game_memory[0] == game_memory[1] == game_memory[2])
    second_line = game_memory[3] != 0 and (game_memory[3] == game_memory[4] == game_memory[5])
    third_line = game_memory[6] != 0 and (game_memory[6] == game_memory[7] == game_memory[8])
    first_column = game_memory[0] != 0 and (game_memory[0] == game_memory[3] == game_memory[6])
    second_column = game_memory[1] != 0 and (game_memory[1] == game_memory[4] == game_memory[7])
    third_column = game_memory[2] != 0 and (game_memory[2] == game_memory[5] == game_memory[8])
    lr_diag = game_memory[0] != 0 and (game_memory[0] == game_memory[4] == game_memory[8])
    rl_diag = game_memory[2] != 0 and (game_memory[2] == game_memory[4] == game_memory[6])
    return first_line or second_line or third_line or first_column or second_column or third_column or lr_diag or rl_diag

def tie_condition():
    full_board = True
    for i in game_memory:
        if i == 0:
            full_board = False
            break
    return full_board

def action_result(x : int, y : int):
    global game_memory
    win = False
    switch = False
    if x != 0 and y != 0:
        nb = num_case(x, y)
        if game_memory[nb] == 0:
            switch = True
            add_player_token(x, y)
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

igs.service_call("DuelEngine", "gameUnregister", (), "")

sleep(1) # Ensure call

igs.stop()