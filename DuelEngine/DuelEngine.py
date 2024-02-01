from math import floor
import ingescape as igs
from time import sleep
import pygetwindow as pgw 
import json
import threading

### CONSTANTS
NAME = "DuelEngine"
SELECT_GAME = "Sélectionnez un jeu !"
REPLAY_GAME = "Souhaitez-vous rejouer ?"
COLOR_MENU = "Changez les couleurs des joueurs !"
SELECT_GAME_STATE = "selectGame"
REPLAY_GAME_STATE = "replayGame"
COLOR_MENU_STATE = "colorMenu"
MAX_GAMES = 4 # Should be equal to board_col * board_row of SELECT_GAME_STATE_INFOS
SELECT_GAME_STATE_INFOS = {"length":300, "height":300, "board_col":2, "board_row":2}
REPLAY_GAME_STATE_INFOS = {"length":135, "height":55, "board_col":1, "board_row":3}
COLORS_AVAILABLES = ["#0048ba","#a52a2a","#66cdaa","#f2b31c","#ffefdb","#ffc0cb","#9966cc","#cccccc","#7fffd4"]
COLOR_MENU_STATE_INFOS = {"length":60, "height":60, "board_col":9, "board_row":9}
BACKGROUND_COLOR = "#FFFFFF"
TOUR_J1 = "Joueur 1 commence son tour."
TOUR_J2 = "Joueur 2 commence son tour."
VICTOIRE_J1 = "Joueur 1 a remporté la victoire !"
VICTOIRE_J2 = "Joueur 2 a remporté la victoire !"
EGALITE = "Match nul !"
W_Y_BORDER_TOP = 128
W_X_BORDER_RIGHT = 408
GAME_UNREGISTERED_DURING_GAME = "ERREUR : Le moteur du jeu a cessé de répondre. Retour à la sélection..."
### --- CONSTANTS

def input_callback(iop_type, name, value_type, value, my_data):
    match name:
        case "click":
            click(igs.input_int("mouse_x"),igs.input_int("mouse_y"))
        case "player1_turn":
            player_turn(0)
        case "player2_turn":
            player_turn(1)
        case "player1_win":
            player_win(0)
        case "player2_win":
            player_win(1)
        case "tie":
            tie()
        case _:
            None

def service_callback(sender_agent_name, sender_agent_uuid, service_name, arguments, token, my_data):
    match (sender_agent_name, service_name):
        case (sender_agent_name,"gameRegister"):
            if not arguments[0] in games_available: # Game not already added
                games_available[arguments[0]] = {"board":arguments[1], "game_image":arguments[2], "length":int(arguments[3]), "height":int(arguments[4]),"board_col":int(arguments[5]), "board_row":int(arguments[6])}
                if current_game == SELECT_GAME_STATE: # If we are selecting a game
                    select_game() # Refresh the select screen to display the new game
        case (sender_agent_name,"gameUnregister"):
            if sender_agent_name in games_available: # Game already added
                del games_available[sender_agent_name]
                if current_game == SELECT_GAME_STATE: # If we are selecting
                    select_game() # Refresh the select screen not to display the old game
            if current_game == sender_agent_name or (current_game == REPLAY_GAME_STATE and last_game_played == sender_agent_name):
                select_game()
                send_log(GAME_UNREGISTERED_DURING_GAME)
        case (sender_agent_name,"addShape"):
            if sender_agent_name == current_game:
                color_fill = arguments[5]
                stroke_color = arguments[6]
                if color_fill == "PLAYER1COLOR":
                    color_fill = players_color[0]
                if color_fill == "PLAYER2COLOR":
                    color_fill = players_color[1]
                if stroke_color == "PLAYER1COLOR":
                    stroke_color = players_color[0]
                if stroke_color == "PLAYER2COLOR":
                    stroke_color = players_color[1]
                infos = {"shape":arguments[0], "x":arguments[1], "y":arguments[2], "width":arguments[3], "height":arguments[4], "color_fill":color_fill,"stroke_color":stroke_color}
                add_element("shape", infos)
        case (sender_agent_name,"addShapeInBoard"):
            if sender_agent_name == current_game:
                add_shape_in_board(arguments[0],arguments[1],arguments[2],arguments[3],arguments[4])
        case (sender_agent_name,"addTextInBoard"):
            if sender_agent_name == current_game:
                add_text_in_board(arguments[0],arguments[1],arguments[2],arguments[3])
        case (sender_agent_name,"addImageurlInBoard"):
            if sender_agent_name == current_game:
                add_shape_in_board(arguments[0],arguments[1],arguments[2])
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
        case _:
            None

def on_agent_event_callback(event, uuid, name, event_data, my_data): ### TBD ###
    ### PARTIE A DOCUMENTER : SI DEUXIEME WHITEBOARD ALORS SORTIE SUR OUTPUT POUR TOUS
    # Whiteboard aurait du avoir un service à appeler afin de cibler l'agent qui envoie l'event
    # Solution : OUTPUT Safe => renvoyer l'état courant qui est connu de tous, le titre le fond etc mais pas l'état initial
    if event == igs.AGENT_KNOWS_US and name == "Whiteboard":
        output_current_state() #updateNewWhiteboard
    if event == igs.AGENT_EXITED:
        if name in games_available: # Game already added
            del games_available[name]
            if current_game == SELECT_GAME_STATE: # If we are selecting a game
                select_game() # Refresh the select screen not to display the old game
        if current_game == name or (current_game == REPLAY_GAME_STATE and last_game_played == name):
            select_game()
            send_log(GAME_UNREGISTERED_DURING_GAME)

def agent_init():
    ### AGENT DEFINITION
    # Name
    igs.agent_set_name(NAME)
    # Inputs
    igs.input_create("mouse_x", igs.INTEGER_T, None)
    igs.input_create("mouse_y", igs.INTEGER_T, None)
    igs.input_create("click", igs.IMPULSION_T, None)
    igs.input_create("player1_win", igs.IMPULSION_T, None)
    igs.input_create("player2_win", igs.IMPULSION_T, None)
    igs.input_create("tie", igs.IMPULSION_T, None)
    igs.input_create("player1_turn", igs.IMPULSION_T, None)
    igs.input_create("player2_turn", igs.IMPULSION_T, None)
    # Inputs callback
    igs.observe_input("click", input_callback, None)
    igs.observe_input("player1_win", input_callback, None)
    igs.observe_input("player2_win", input_callback, None)
    igs.observe_input("tie", input_callback, None)
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
    igs.service_arg_add("gameRegister", "height", igs.INTEGER_T)
    igs.service_arg_add("gameRegister", "board_col", igs.INTEGER_T)
    igs.service_arg_add("gameRegister", "board_row", igs.INTEGER_T)
    igs.service_init("gameUnregister", service_callback, None)
    igs.service_init("addShape", service_callback, None)
    igs.service_arg_add("addShape", "shape", igs.STRING_T)
    igs.service_arg_add("addShape", "x", igs.INTEGER_T)
    igs.service_arg_add("addShape", "y", igs.INTEGER_T)
    igs.service_arg_add("addShape", "width", igs.INTEGER_T)
    igs.service_arg_add("addShape", "height", igs.INTEGER_T)
    igs.service_arg_add("addShape", "color_fill", igs.STRING_T)
    igs.service_arg_add("addShape", "stroke_color", igs.STRING_T)
    igs.service_init("addShapeInBoard", service_callback, None)
    igs.service_arg_add("addShapeInBoard", "shape", igs.STRING_T)
    igs.service_arg_add("addShapeInBoard", "x", igs.INTEGER_T)
    igs.service_arg_add("addShapeInBoard", "y", igs.INTEGER_T)
    igs.service_arg_add("addShapeInBoard", "color_fill", igs.STRING_T)
    igs.service_arg_add("addShapeInBoard", "stroke_color", igs.STRING_T)
    igs.service_init("addTextInBoard", service_callback, None)
    igs.service_arg_add("addTextInBoard", "text", igs.STRING_T)
    igs.service_arg_add("addTextInBoard", "x", igs.INTEGER_T)
    igs.service_arg_add("addTextInBoard", "y", igs.INTEGER_T)
    igs.service_arg_add("addTextInBoard", "color", igs.STRING_T)
    igs.service_init("addImageurlInBoard", service_callback, None)
    igs.service_arg_add("addImageurlInBoard", "url", igs.STRING_T)
    igs.service_arg_add("addImageurlInBoard", "x", igs.INTEGER_T)
    igs.service_arg_add("addImageurlInBoard", "y", igs.INTEGER_T)
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

def init():
    global program_running
    program_running = True
    games_available[SELECT_GAME_STATE] = SELECT_GAME_STATE_INFOS # Select menu
    games_available[REPLAY_GAME_STATE] = REPLAY_GAME_STATE_INFOS # Replay menu
    games_available[COLOR_MENU_STATE] = COLOR_MENU_STATE_INFOS # Color menu
    select_game()
    anti_moving_guard = threading.Thread(target=elements_not_transposable)
    anti_moving_guard.start()
    update_whiteboard_infos()

### GLOBAL VARIABLES 
current_title = ""
current_player_color = ""
current_game = ""
last_game_played = ""
program_running = True
games_available = {} # {"Morpion":{"game_image":"screen.url","board":"board.url", "length":20, "height":20, board_col":3, "board_row":3},...}
current_game_selection = [] # Updated in select_game()
current_game_score = [0,0] # [player1score,player2score]
players_color = [COLORS_AVAILABLES[0],COLORS_AVAILABLES[1]] # [player1color,player2color]
current_board_location = [] # top_left_x, top_left_y, bottom_right_x, bottom_right_y
whiteboard_infos = {"x":0,
                    "y":0,
                    "width":0,
                    "height":0}
whiteboard_fixed_elements = []  # {id, type, infos} infos for a shape : {shape, x, y, width, height, color_fill, stroke_color}
### --- GLOBAL VARIABLES

### FUNCTIONS : WITH A IGS CALL

def elements_not_transposable(): ### TBD ### Mentionner ça dans le rapport + essai anti deletion
    global program_running
    while(program_running):
        for element in whiteboard_fixed_elements:
            arguments = (element["id"], float(element["infos"]["x"]), float(element["infos"]["y"]))
            igs.service_call("Whiteboard", "moveTo", arguments, "")
        sleep(0.2)

def output_current_state():
    sleep(2) # Waiting for the Whiteboard to refresh his screen (not my fault)
    igs.output_set_string("title_or_score", current_title)
    igs.output_set_string("currentPlayerColor", current_player_color)
    igs.output_set_string("currentGame", current_game)

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
        update_current_game_board_infos()
    
    igs.output_set_string("title_or_score", current_title)
    igs.output_set_string("currentPlayerColor", current_player_color)
    igs.output_set_string("currentGame", current_game)

def send_log(log : str):
    igs.output_set_string("lastGameLog", log)

def game_action(x : int, y : int):
    igs.output_set_int("x", x)
    igs.output_set_int("y", y)
    igs.output_set_impulsion("gameAction")

def create_shape(shape : str, x : float, y : float, width : float, height : float, color_fill : str, stroke_color : str):
    parameters = (shape, x, y, width, height, color_fill, stroke_color, 1.0)
    igs.service_call("Whiteboard", "addShape", parameters, "")

def create_image_from_url(url : str, x : float, y : float):
    parameters = (url, x, y)
    igs.service_call("Whiteboard", "addImageFromUrl", parameters, "")

def create_text(text : str, x : float, y : float, color : str):
    parameters = (text, x, y, color)
    igs.service_call("Whiteboard", "addText", parameters, "")

def reset_game():
    igs.output_set_impulsion("gameReset")

def clear_whiteboard():
    global whiteboard_fixed_elements
    whiteboard_fixed_elements = []
    igs.service_call("Whiteboard", "clear", None, "")

### --- FUNCTIONS : WITH A IGS CALL
    
### FUNCTIONS : GETTING / MODIFYING INFOS 
    
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

def xy_whiteboard_is_in_board(x : float, y : float):
    x_in = current_board_location[0] < x and x < current_board_location[2]
    y_in = current_board_location[1] < y and y < current_board_location[3]
    return x_in and y_in

def xy_board_is_in_board(x : int, y : int):
    game = games_available[current_game]
    return (x > 0 and x <= game["board_col"] and y > 0 and y <= game["board_row"])

def board_to_whiteboard(x : int, y : int):
    game = games_available[current_game]
    x_whiteboard = (x-1)*game["length"]+current_board_location[0]
    y_whiteboard = (y-1)*game["height"]+current_board_location[1]
    return float(x_whiteboard), float(y_whiteboard)

def whiteboard_to_board(x : float, y : float):
    game = games_available[current_game]
    x_board = floor((x-current_board_location[0])/game["length"]) + 1
    y_board = floor((y-current_board_location[1])/game["height"]) + 1
    return x_board, y_board

def update_current_game_board_infos():
    game = games_available[current_game]
    length = game["length"]
    height = game["height"]
    board_col = game["board_col"]
    board_row = game["board_row"]
    update_board_infos(length, height, board_col, board_row)

def update_board_infos(length : int, height : int, board_col : int, board_row : int):
    global current_board_location
    x_diff = (board_col * length) / 2
    y_diff = (board_row * height) / 2
    whiteboard_width = whiteboard_infos["width"] - W_X_BORDER_RIGHT
    whiteboard_height = whiteboard_infos["height"] - W_Y_BORDER_TOP
    x_center_whiteboard = whiteboard_width / 2
    y_center_whiteboard = whiteboard_height / 2
    top_left_x = x_center_whiteboard - x_diff
    top_left_y = y_center_whiteboard - y_diff
    bottom_right_x = x_center_whiteboard + x_diff
    bottom_right_y = y_center_whiteboard + y_diff
    current_board_location = [top_left_x, top_left_y, bottom_right_x, bottom_right_y]

def get_game_score():
    return "Joueur 1 | " + str(current_game_score[0]) + " - " + str(current_game_score[1]) + " | Joueur 2"

### --- FUNCTIONS : GETTING / MODIFYING INFOS
    
### FUNCTIONS : CALLBACK OF INPUTS
    
def click(x : int, y : int):
    update_whiteboard_infos()
    if is_in_whiteboard(x, y):
        x_whiteboard, y_whiteboard = coord_to_whiteboard(x,y)
        if current_game != SELECT_GAME_STATE and current_game != REPLAY_GAME_STATE and current_game != COLOR_MENU_STATE:
            x_board, y_board = whiteboard_to_board(x_whiteboard, y_whiteboard)
            if not xy_board_is_in_board(x_board, y_board):
                x_board, y_board = 0, 0
            game_action(x_board, y_board)
        else:
            if current_game == SELECT_GAME_STATE:
                select_action(x_whiteboard, y_whiteboard)
            else:
                if current_game == REPLAY_GAME_STATE:
                    replay_action(x_whiteboard, y_whiteboard)
                else:
                    color_action(x_whiteboard, y_whiteboard)

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
    end_of_game()

def tie():
    update_current_state(EGALITE, BACKGROUND_COLOR, None)
    send_log(EGALITE)
    end_of_game()

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
    
def add_element(elementType : str, infos):
    match elementType:
        case "shape":
            create_shape(infos["shape"], float(infos["x"]), float(infos["y"]), float(infos["width"]), float(infos["height"]), infos["color_fill"], infos["stroke_color"])     
        case "imageurl":
            create_image_from_url(infos["url"], float(infos["x"]), float(infos["y"]))
        case "text":
            create_text(infos["text"], float(infos["x"]), float(infos["y"]), infos["color"])
        case _:
            None

def add_text_in_board(text : str, x : int, y : int, color : str):
    if xy_board_is_in_board(x, y):
        x_whiteboard, y_whiteboard = board_to_whiteboard(x, y)
        infos = {"text":text, "x":x_whiteboard+4, "y":y_whiteboard+4, "color":color}
        add_element("text", infos)

def add_shape_in_board(shape : str, x : int, y : int, color_fill : str, stroke_color : str):
    if xy_board_is_in_board(x, y):
        if color_fill == "PLAYER1COLOR":
            color_fill = players_color[0]
        if color_fill == "PLAYER2COLOR":
            color_fill = players_color[1]
        if stroke_color == "PLAYER1COLOR":
            stroke_color = players_color[0]
        if stroke_color == "PLAYER2COLOR":
            stroke_color = players_color[1]
        game = games_available[current_game]
        x_whiteboard, y_whiteboard = board_to_whiteboard(x, y)
        infos = {"shape":shape, "x":x_whiteboard+4, "y":y_whiteboard+4, "width":game["length"]-8, "height":game["height"]-8, "color_fill":color_fill,"stroke_color":stroke_color}
        add_element("shape", infos)

def add_imageurl_in_board(url : str, x : int, y : int):
    if xy_board_is_in_board(x, y):
        x_whiteboard, y_whiteboard = board_to_whiteboard(x, y)
        infos = {"url":url, "x":x_whiteboard, "y":y_whiteboard}
        add_element("imageurl", infos)

### --- FUNCTIONS : HELPERS (WHITEBOARD)
    
### FUNCTIONS : CORE PROGRAM

def select_game():
    clear_whiteboard()
    update_current_state(SELECT_GAME, BACKGROUND_COLOR, SELECT_GAME_STATE)
    send_log(SELECT_GAME)
    add_element("text",{"text":"Menu des couleurs","x":0,"y":0,"color":"black"})
    if len(games_available) > 2: # Because SELECT_GAME_STATE, REPLAY_GAME_STATE and COLOR_MENU_STATE are in
        global current_game_selection
        current_game_selection = []
        nb = 1
        col = games_available[SELECT_GAME_STATE]["board_col"]
        row = games_available[SELECT_GAME_STATE]["board_row"]
        if (col * row) != MAX_GAMES:
            print("INTERNAL ERROR: MAX GAMES DOES NOT MATCH COL AND ROW OF SELECT_GAME_STATE_INFOS")
            exit(1)
        for game in games_available:
            if game != SELECT_GAME_STATE and game != REPLAY_GAME_STATE and game != COLOR_MENU_STATE:
                if nb <= MAX_GAMES:
                    current_game_selection.append(game)
                    game_col = nb % (col+1)
                    game_row = floor(nb/(row+1))+1
                    add_shape_in_board("rectangle", game_col, game_row, BACKGROUND_COLOR, "black")
                    add_imageurl_in_board(games_available[game]["game_image"], game_col, game_row)
                else: # More than 9 games
                    break
                nb = nb + 1

def replay_game():
    clear_whiteboard()
    update_current_state(None, None, REPLAY_GAME_STATE)
    send_log(REPLAY_GAME)
    add_shape_in_board("rectangle", 1, 1, BACKGROUND_COLOR, "green")
    add_text_in_board("Rejouer", 1, 1, "black")
    add_shape_in_board("rectangle", 1, 3, BACKGROUND_COLOR, "red")
    add_text_in_board("Quitter", 1, 3, "black")

def color_menu():
    clear_whiteboard()
    update_current_state(COLOR_MENU, None, COLOR_MENU_STATE)
    send_log(COLOR_MENU)
    add_text_in_board("Couleur du joueur 1", 1, 1, "black")
    add_text_in_board("Couleur du joueur 2", 1, 5, "black")
    add_text_in_board("Quitter", 5, 9, "black")
    nb = 1
    for color in COLORS_AVAILABLES:
        add_shape_in_board("rectangle",nb,3,color,"black")
        add_shape_in_board("rectangle",nb,7,color,"black")
        nb = nb + 1

def select_action(x : float, y : float):
    if x < 300.0 and y < 50.0: # Color menu
        color_menu()
    else:
        x_board, y_board = whiteboard_to_board(x, y)
        if xy_board_is_in_board(x_board, y_board):
            col = games_available[SELECT_GAME_STATE]["board_col"]
            num = (x_board + col*(y_board-1)) - 1
            if num < len(current_game_selection):
                play(current_game_selection[num])

def replay_action(x : int, y : int):
    x_board, y_board = whiteboard_to_board(x, y)
    if xy_board_is_in_board(x_board, y_board):
        if x_board == 1 and y_board == 1: # If replay
            play(last_game_played)
        if x_board == 1 and y_board == 3: # If leave 
            set_game_score(0,0)
            select_game()

def color_action(x : int, y :int):
    x_board, y_board = whiteboard_to_board(x, y)
    if xy_board_is_in_board(x_board, y_board):
        if (x_board == 5 or x_board == 6) and y_board == 9: # If leave
            select_game()
        if y_board == 3:
            players_color[0] = COLORS_AVAILABLES[x_board-1]
            update_current_state(None,players_color[0],None)
            send_log("Couleur du joueur 1 modifiée !")
        if y_board == 7:
            players_color[1] = COLORS_AVAILABLES[x_board-1]
            update_current_state(None,players_color[1],None)
            send_log("Couleur du joueur 2 modifiée !")


def end_of_game():
    set_last_game_played()
    replay_game()

def set_last_game_played():
    global last_game_played
    last_game_played = current_game

def set_game_score(player1_score : int, player2_score : int):
    global current_game_score
    if player1_score != None :
        current_game_score[0] = player1_score
    if player2_score != None :
        current_game_score[1] = player2_score

def play(game : str):
    clear_whiteboard()
    update_current_state(get_game_score(), None, game)
    send_log("Début d'une partie de : " + current_game)
    reset_game()
    add_element("imageurl",{"url":games_available[current_game]["board"],"x":current_board_location[0],"y":current_board_location[1]})

### --- FUNCTIONS : CORE PROGRAM

agent_init()

sleep(1) # Ensure agent initialisation before starting program

init()

print(NAME)

input()

program_running = False

igs.stop()