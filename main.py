from game import Game

rounds = 12
root = None
input_text = "y"

while input_text == "y":
    game = Game(root, rounds)
    input_text = input("Press \"y\" to restart game, or something else if NOT: ")