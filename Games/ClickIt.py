#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  ClickIt version 1.0
#  Created by Ingenuity i/o on 2024/01/30
#

import sys
from time import sleep
import ingescape as igs

NAME = "ClickIt"

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
    igs.definition_set_description("""A simple game that consists in clicking in the square""")
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
BOARD = "https://github.com/ArnaudN7/DuelEngine/blob/main/Games/Images/ClickIt.png?raw=true"
GAME_IMAGE = "https://play-lh.googleusercontent.com/zPxLgj5nvl20ahJV7aFC6S5mD8kii5CEEDj25j1P9CYAfXL9sdDuO-8eES0r4DhJHrU"
CASE_LENGTH = 200
BOARD_COL = 3
BOARD_ROW = 3
player1_started_last_game = False
player1_turn = True
### --- GLOBAL VARIABLES

### FUNCTIONS : WITH A IGS CALL
def player_turn():
    next_turn = "player1_turn" if player1_turn else "player2_turn"
    igs.output_set_impulsion(next_turn)

def player_win():
    winner = "player1_win" if player1_turn else "player2_win"
    igs.output_set_impulsion(winner)
### --- FUNCTIONS : WITH A IGS CALL
    
### FUNCTIONS : CALLBACK OF INPUTS
def game_action(x : int, y : int):
    if action_result(x, y):
        player_win()
    else:
        switch_player_turn()
        player_turn()

def game_reset():
    global player1_turn
    global player1_started_last_game
    player1_turn = not player1_started_last_game
    player1_started_last_game = not player1_started_last_game
    player_turn()
### --- FUNCTIONS : CALLBACK OF INPUTS

### FUNCTIONS : CORE PROGRAM
def switch_player_turn():
    global player1_turn
    player1_turn = not player1_turn

def action_result(x : int, y : int):
    win = False
    if x == 2 and y == 2:
        win = True
    return win
### --- FUNCTIONS : CORE PROGRAM

init()

print(NAME)

input()

igs.service_call("DuelEngine", "gameUnregister", (), "")

sleep(1) # Ensure call

igs.stop()