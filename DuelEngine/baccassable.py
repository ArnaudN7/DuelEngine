dict = {"oui":0}

def func():
    print("oui" in dict)
    del dict["oui"]

func()

print(dict)
# {"Morpion":{"game_image":"screen.url","board":"board.url", "length":20, "height":20, board_col":3, "board_row":3},...}