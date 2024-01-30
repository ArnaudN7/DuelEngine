from math import floor
import ingescape as igs
from time import sleep
import pygetwindow as pgw 
import json
import threading

### CONSTANTS
NAME = "DuelEngine"
SELECT_GAME = "Sélectionnez un jeu !"
BACKGROUND_COLOR = "#FFFFFF"
TOUR_J1 = "Joueur 1 commence son tour."
TOUR_J2 = "Joueur 2 commence son tour."
VICTOIRE_J1 = "Joueur 1 a remporté la victoire !"
VICTOIRE_J2 = "Joueur 2 a remporté la victoire !"
SELECT_GAME_STATE = "selectGame"
W_Y_BORDER_TOP = 128
W_X_BORDER_RIGHT = 408
### --- CONSTANTS

def input_callback(iop_type, name, value_type, value, my_data):
    match name:
        case "click":
            click(igs.input_int("mouse_x"),igs.input_int("mouse_y"))
            None
        case "player1_turn":
            player_turn(0)
        case "player2_turn":
            player_turn(1)
        case "player1_win":
            player_win(0)
        case "player2_win":
            player_win(1)
        case _:
            None

def service_callback(sender_agent_name, sender_agent_uuid, service_name, arguments, token, my_data):
    match (sender_agent_name, service_name):
        case (sender_agent_name,"gameRegister"):
            global games_available
            games_available[arguments[0]] = {"board":arguments[1], "game_image":arguments[2], "length":int(arguments[3]), "board_col":int(arguments[4]), "board_row":int(arguments[5])}
        case ("Whiteboard","elementCreated"):
            igs.service_call("Whiteboard", "getElements", None, "")
        case ("Whiteboard","elements"):
            arguments_json = json.loads(arguments[0])
            for element in range(len(arguments_json)):
                current_element = arguments_json[element]
                found = False
                for ele in whiteboard_fixed_elements:
                    if ele["id"] == current_element["id"]:
                        found = True
                        break
                if not found:
                    whiteboard_fixed_elements.append({"id":current_element["id"],"type":current_element["type"],"infos":current_element})
        case ("Whiteboard","actionResult"): ### TBD ###
            None # SET STATE TO ERROR DELETION, ASK FOR ALL ELEMENTS AND ADDSHAPE SHAPES IN WHITEBOARDFIXED AND NOT IN ALLELEMENTS
            # OTHER OPTION, MODIFY "elements" receiver with this behavior and just trigger getElements
        case _:
            None

def on_agent_event_callback(event, uuid, name, event_data, my_data): ### TBD ###
    ### PARTIE A DOCUMENTER : SI DEUXIEME WHITEBOARD ALORS SORTIE SUR OUTPUT POUR TOUS
    # Whiteboard aurait du avoir un service à appeler afin de cibler l'agent qui envoie l'event
    #Solution : OUTPUT Safe => renvoyer l'état courant qui est connu de tous, le titre le fond etc mais pas l'état initial
    if event == igs.AGENT_KNOWS_US and name == "Whiteboard":
        output_current_state() #updateNewWhiteboard

def agent_init():
    ### AGENT DEFINITION
    igs.input_create("forDev", igs.IMPULSION_T, None)
    igs.observe_input("forDev", forDev, None)
    # Name
    igs.agent_set_name(NAME)
    # Inputs
    igs.input_create("mouse_x", igs.INTEGER_T, None)
    igs.input_create("mouse_y", igs.INTEGER_T, None)
    igs.input_create("click", igs.IMPULSION_T, None)
    igs.input_create("player1_win", igs.IMPULSION_T, None)
    igs.input_create("player2_win", igs.IMPULSION_T, None)
    igs.input_create("player1_turn", igs.IMPULSION_T, None)
    igs.input_create("player2_turn", igs.IMPULSION_T, None)
    # Inputs callback
    igs.observe_input("click", input_callback, None)
    igs.observe_input("player1_win", input_callback, None)
    igs.observe_input("player2_win", input_callback, None)
    igs.observe_input("player1_turn", input_callback, None)
    igs.observe_input("player2_turn", input_callback, None)
    # Outputs
    igs.output_create("title_or_score", igs.STRING_T, None)
    igs.output_create("currentPlayerColor", igs.STRING_T, None)
    igs.output_create("lastGameLog", igs.STRING_T, None)
    igs.output_create("currentGame", igs.STRING_T, None)
    igs.output_create("x", igs.INTEGER_T, None)
    igs.output_create("y", igs.INTEGER_T, None)
    igs.output_create("gameAction", igs.IMPULSION_T, None)
    igs.output_create("gameReset", igs.IMPULSION_T, None)
    ### Services
    # Create
    igs.service_init("gameRegister", service_callback, None)
    igs.service_arg_add("gameRegister", "gameName", igs.STRING_T)
    igs.service_arg_add("gameRegister", "game_image", igs.STRING_T)
    igs.service_arg_add("gameRegister", "board", igs.STRING_T)
    igs.service_arg_add("gameRegister", "length", igs.INTEGER_T)
    igs.service_arg_add("gameRegister", "board_col", igs.INTEGER_T)
    igs.service_arg_add("gameRegister", "board_row", igs.INTEGER_T)
    # Receive
    igs.service_init("elementCreated", service_callback, None)
    igs.service_arg_add("elementCreated", "elementId", igs.INTEGER_T)
    igs.service_init("elements", service_callback, None)
    igs.service_arg_add("elements", "jsonArray", igs.STRING_T)
    igs.service_init("actionResult", service_callback, None)
    igs.service_arg_add("succeeded", "bool", igs.BOOL_T)
    # Observe agent
    igs.observe_agent_events(on_agent_event_callback, None)
    # Connection
    igs.start_with_device("Loopback Pseudo-Interface 1", 5670)

def output_current_state():
    igs.output_set_string("title_or_score", current_title)
    igs.output_set_string("currentPlayerColor", current_player_color)
    igs.output_set_string("currentGame", current_game)

def select_game():
    global current_title
    global current_player_color
    global current_game
    current_title = SELECT_GAME
    igs.output_set_string("title_or_score", current_title)
    current_player_color = BACKGROUND_COLOR
    igs.output_set_string("currentPlayerColor", current_player_color)
    igs.output_set_string("lastGameLog", SELECT_GAME)
    current_game = SELECT_GAME_STATE
    igs.output_set_string("currentGame", current_game)

def init():
    global program_running
    program_running = True
    select_game()
    elements_guard = threading.Thread(target=elements_not_transposable)
    elements_guard.start()
    update_whiteboard_infos()

def forDev(iop_type, name, value_type, value, my_data): ### TEMP ###
    play("ClickIt")

### GLOBAL VARIABLES 
current_title = ""
current_player_color = ""
current_game = ""
program_running = True
games_available = {} # {"Morpion":{"game_image":"screen.url","board":"board.url", "length":20, "board_col":3, "board_row":3},...}
current_game_score = [0,0] # [player1score,player2score]
players_color = ["#F9F9F9","#023124"] # [player1color,player2color]
current_board_location = [] # top_left_x, top_left_y, bottom_right_x, bottom_right_y
whiteboard_infos = {"x":0,
                    "y":0,
                    "width":0,
                    "height":0}
whiteboard_fixed_elements = []  # {id, type, infos} infos for a shape : {shape, x, y, width, height, color_fill, stroke_color}
### --- GLOBAL VARIABLES

### FUNCTIONS WITH A IGS CALL

def elements_not_transposable():
    global program_running
    while(program_running):
        for element in whiteboard_fixed_elements:
            arguments = (element["id"], float(element["infos"]["x"]), float(element["infos"]["y"]))
            igs.service_call("Whiteboard", "moveTo", arguments, "")
        sleep(0.2)

def update_current_state(title : str, player_color : str, game : str):
    if title != None:
        global current_title
        current_title = title
    if player_color != None:
        global current_player_color
        current_player_color = player_color
    if game != None:
        global current_game
        current_game = game
    
    igs.output_set_string("title_or_score", current_title)
    igs.output_set_string("currentPlayerColor", current_player_color)
    igs.output_set_string("currentGame", current_game)

def send_log(log : str):
    igs.output_set_string("lastGameLog", log)

def game_action(x : int, y : int):
    x_out = 0
    y_out = 0
    x_in = current_board_location[0] < x and x < current_board_location[2]
    y_in = current_board_location[1] < y and y < current_board_location[3]
    if x_in and y_in:
        game = games_available[current_game]
        x_out = floor((x-current_board_location[0])/game["length"]) + 1
        y_out = floor((y-current_board_location[1])/game["length"]) + 1
    igs.output_set_int("x", int(x_out))
    igs.output_set_int("y", int(y_out))
    igs.output_set_impulsion("gameAction")

def create_shape(shape : str, x : float, y : float, width : float, height : float, color_fill : str, stroke_color : str):
    parameters = (shape, x, y, width, height, color_fill, stroke_color, 0.0)
    igs.service_call("Whiteboard", "addShape", parameters, "")

def create_image_from_url(url : str, x : float, y : float):
    parameters = (url, x, y)
    igs.service_call("Whiteboard", "addImageFromUrl", parameters, "")

def reset_game():
    igs.output_set_impulsion("gameReset")

### --- FUNCTIONS WITH A IGS CALL
    
### FUNCTIONS : GETTING INFOS 
def update_whiteboard_infos():
    window = pgw.getWindowsWithTitle("Whiteboard")
    if window:
        global whiteboard_infos
        whiteboard_infos = {"x":window[0].left,
                "y":window[0].top,
                "width":window[0].width,
                "height":window[0].height}

def is_in_whiteboard(x : int, y : int):
    return (x >= whiteboard_infos["x"] and y >= whiteboard_infos["y"]+W_Y_BORDER_TOP and x <= whiteboard_infos["x"]+whiteboard_infos["width"]-W_X_BORDER_RIGHT and y <= whiteboard_infos["y"]+whiteboard_infos["height"])

def coord_to_whiteboard(x : int, y : int):
    return float(x - (whiteboard_infos["x"]+6)), float(y - (whiteboard_infos["y"]+W_Y_BORDER_TOP))

def update_board_infos():
    global current_board_location
    length = games_available[current_game]["length"]
    x_diff = (games_available[current_game]["board_col"] * length) / 2
    y_diff = (games_available[current_game]["board_row"] * length) / 2
    whiteboard_width = whiteboard_infos["width"] - W_X_BORDER_RIGHT
    whiteboard_height = whiteboard_infos["height"] - W_Y_BORDER_TOP
    x_center_whiteboard = whiteboard_width / 2
    y_center_whiteboard = whiteboard_height / 2
    top_left_x = x_center_whiteboard - x_diff
    top_left_y = y_center_whiteboard - y_diff
    bottom_right_x = x_center_whiteboard + x_diff
    bottom_right_y = y_center_whiteboard + y_diff
    current_board_location = [top_left_x, top_left_y, bottom_right_x, bottom_right_y]
    ### TEMP ###
    add_element("shape",{"shape":"rectangle","x":top_left_x,"y":top_left_y,"width":length*3,"height":length*3,"color_fill":"blue","stroke_color":"black"})

def get_game_score():
    return "Joueur 1 | " + str(current_game_score[0]) + " - " + str(current_game_score[1]) + " | Joueur 2"

### --- FUNCTIONS : GETTING INFOS
    
### FUNCTIONS : CALLBACK OF INPUTS
    
def click(x : int, y : int):
    update_whiteboard_infos()
    if is_in_whiteboard(x, y):
        new_x, new_y = coord_to_whiteboard(x,y)
        game_action(new_x, new_y)

def player_win(player_id : int): # player_id : 0 or 1
    text_win = ""
    if player_id == 0:
        text_win = VICTOIRE_J1
        set_game_score(current_game_score[0] + 1, None)
    else:
        text_win = VICTOIRE_J2
        set_game_score(None, current_game_score[1] + 1)
    update_current_state(text_win, BACKGROUND_COLOR, None)
    send_log(text_win)


def player_turn(player_id : int): # player_id : 0 or 1
    game_log = ""
    if player_id == 0:
        game_log = TOUR_J1
    else:
        game_log = TOUR_J2
    update_current_state(None, players_color[player_id], None)
    send_log(game_log)

### --- FUNCTIONS : CALLBACK OF INPUTS
    
### FUNCTIONS : HELPERS (WHITEBOARD)
    
def add_element(elementType : float, infos):
    match elementType:
        case "shape":
            create_shape(infos["shape"], float(infos["x"]), float(infos["y"]), float(infos["width"]), float(infos["height"]), infos["color_fill"], infos["stroke_color"])     
        case "imageurl":
            create_image_from_url(infos["url"], float(infos["x"]), float(infos["y"]))
        case _:
            None

### --- FUNCTIONS : HELPERS (WHITEBOARD)
    
### FUNCTIONS : CORE PROGRAM

def set_game_score(player1_score : int, player2_score : int):
    global current_game_score
    if player1_score != None :
        current_game_score[0] = player1_score
    if player2_score != None :
        current_game_score[1] = player2_score

def play(game : str):
    if game != SELECT_GAME_STATE:
        update_current_state(get_game_score(), None, game)
        send_log("Début d'une partie de : " + current_game)
        reset_game()
        update_board_infos()
        add_element("imageurl",{"url":games_available[current_game]["board"],"x":current_board_location[0],"y":current_board_location[1]})
    else:
        select_game()

def end_of_game():
    # Afficher bouton retry
    # Attendre click sur un bouton
    # Si rejouer alors
    play(current_game)
    # Sinon revenir à la selection de jeu
    set_game_score(0,0)
    play(SELECT_GAME_STATE)

### --- FUNCTIONS : CORE PROGRAM

agent_init()

init()

print(NAME)

input()

program_running = False

igs.stop()