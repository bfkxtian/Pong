# Pong
Pong in PyGame

Classic arcade game of Pong in Python w/ Pygame

Controls:
  SINGLEPLAYER:
    'w' and 's': move up and down (left)
  MULTIPLAYER:
    'w' and 's': move up and down (player 1, server - left )
    'o' and 'l': move up and down (player2, client - right )
  
  Issues:
    Does not seem to connect on separate machines (local machines are fine)
    Gameplay can 'desynchronise' between machines (is_moving is only data being sent)
    Ball velocity is not constant at all angles (poor use of trigonometric calculations)
