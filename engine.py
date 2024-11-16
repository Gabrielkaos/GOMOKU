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

def get_row_col(square):
    if not 0 <= square <= BOARD_ROW * BOARD_COLUMN:
        raise ValueError(f"Square number must be between 0 and {BOARD_ROW * BOARD_COLUMN}.")
    row = square // BOARD_ROW
    col = square % BOARD_COLUMN
    
    return row, col


class Undo:
    def __init__(self):
        self.row = None
        self.col = None


class Engine:
    def __init__(self):
        self.board = [[EMPTY for _ in range(BOARD_COLUMN)] for _ in range(BOARD_ROW)]
        self.side = WHITE
        self.moves_made = 0
        self.history_of_moves = [Undo() for _ in range(BOARD_ROW*BOARD_COLUMN)]

    def is_winning(self, color):
        for i in range(BOARD_ROW * BOARD_COLUMN):
            row, col = get_row_col(i)
                
            #if we found a piece
            if self.board[row][col] == color:
                #check directions
                for dir in DIRECTIONS:
                    piece_connected = 1
                    new_row, new_col = row, col
                    for _ in range(4):
                        new_row -= dir[0]
                        new_col -= dir[1]

                        #check if out of bounds
                        if (new_row < 0 or new_row >= BOARD_ROW) or \
                            (new_col < 0 or new_col >= BOARD_COLUMN):
                            break
                        #check if the same piece
                        if self.board[new_row][new_col]==color:
                            piece_connected+=1
                        else:
                            break
                    
                    if piece_connected==5:
                        return True
        return False
    
    def evaluate(self, color):
        evaluation = 0

        for i in range(BOARD_ROW * BOARD_COLUMN):
            row, col = get_row_col(i)
                
            #if we found a piece
            if self.board[row][col] == color:
                #check directions
                for dir in DIRECTIONS:
                    piece_connected = 1
                    new_row, new_col = row, col
                    for _ in range(4):
                        new_row -= dir[0]
                        new_col -= dir[1]

                        #check if out of bounds
                        if (new_row < 0 or new_row >= BOARD_ROW) or \
                            (new_col < 0 or new_col >= BOARD_COLUMN):
                            break
                        #check if the same piece
                        if self.board[new_row][new_col]==color:
                            piece_connected+=1
                        else:
                            break
                    
                    evaluation += piece_connected
                    
        return piece_connected
    
    def get_reverse_side(self):
        if self.side==WHITE:
            return BLACK
        return WHITE

    def _reverse_side(self):
        if self.side==WHITE:
            self.side=BLACK
        else:self.side=WHITE

    def pretty_print(self):
        print("Board:")
        for i in range(BOARD_ROW):
            for j in range(BOARD_COLUMN):
                print(PIECE_CHAR[self.board[i][j]]," ", end="")
            print()
        
        print("Side to move:",PIECE_CHAR[self.side])

    def make_move(self, row, col):
        #if not empty make the move
        if self.board[row][col]==EMPTY:
            #place piece
            self.board[row][col] = self.side

            #history of moves
            self.history_of_moves[self.moves_made].row = row
            self.history_of_moves[self.moves_made].col = col

            #increment the move counter
            self.moves_made+=1

            #reverse side
            self._reverse_side()
            return True
        return False

    def undo_move(self):
        if self.moves_made>0:
            self.moves_made-=1
            last_move = self.history_of_moves[self.moves_made]

            self.board[last_move.row][last_move.col] = EMPTY

            self._reverse_side()

        else:
            raise Exception("No moves made")




if __name__ == "__main__":
    engine = Engine()