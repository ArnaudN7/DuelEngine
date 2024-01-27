import pygetwindow as pgw

fenetre = pgw.getWindowsWithTitle("Whiteboard")

if fenetre:
    print(fenetre[0])