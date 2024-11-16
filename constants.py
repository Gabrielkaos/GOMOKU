EMPTY = 0
WHITE = 1
BLACK = 2
BOARD_ROW    = 15
BOARD_COLUMN = 15
PIECE_CHAR = {EMPTY:".", WHITE:"w", BLACK:"b"}
DIRECTIONS = [
    (1,0), #down
    (-1,0), #up
    (0,1), #right
    (0,-1), #left
    (1,1), #SE
    (-1,1), #NE
    (-1,-1), #NW
    (1,-1) #SW
]