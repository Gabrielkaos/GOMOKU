import pygame
from engine import Engine


EMPTY = 0
WHITE = 1
BLACK = 2
BOARD_ROW    = 15
BOARD_COLUMN = 15
PIECE_CHAR = {EMPTY:".", WHITE:"w", BLACK:"b"}


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
CELL_SIZE = SCREEN_WIDTH // BOARD_COLUMN
LINE_COLOR = (255, 255, 255)
BACKGROUND_COLOR = (0 , 0, 0)
WHITE_PIECE_COLOR = (255, 0, 0)
BLACK_PIECE_COLOR = (0, 0, 255)
FPS = 30

class GomokuGUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Gomoku")
        self.clock = pygame.time.Clock()
        self.running = True
        self.engine = Engine()
        self.ai = BLACK

    def draw_board(self):
        self.screen.fill(BACKGROUND_COLOR)
        for row in range(BOARD_ROW + 1):
            pygame.draw.line(
                self.screen, LINE_COLOR, 
                (0, row * CELL_SIZE), 
                (SCREEN_WIDTH, row * CELL_SIZE)
            )
        for col in range(BOARD_COLUMN + 1):
            pygame.draw.line(
                self.screen, LINE_COLOR, 
                (col * CELL_SIZE, 0), 
                (col * CELL_SIZE, SCREEN_HEIGHT)
            )

    def draw_pieces(self):
        for row in range(BOARD_ROW):
            for col in range(BOARD_COLUMN):
                piece = self.engine.board[row][col]
                if piece != EMPTY:
                    piece_color = WHITE_PIECE_COLOR if piece == WHITE else BLACK_PIECE_COLOR
                    center = (
                        col * CELL_SIZE + CELL_SIZE // 2,
                        row * CELL_SIZE + CELL_SIZE // 2
                    )
                    pygame.draw.circle(self.screen, piece_color, center, CELL_SIZE // 3)

    def handle_click(self, pos):
        x, y = pos
        col = x // CELL_SIZE
        row = y // CELL_SIZE

        if 0 <= row < BOARD_ROW and 0 <= col < BOARD_COLUMN:
            if self.engine.make_move(row, col):
                if self.engine.is_winning(self.engine.get_reverse_side()):
                    print(f"{PIECE_CHAR[self.engine.get_reverse_side()]} wins!")
                    self.running = False

    def handle_ai(self):
        best_score, best_move = negamax_with_alphabeta(self.engine, depth=3, alpha=float('-inf'), beta=float('inf'), color=1)
        print(f"Best move: {best_move}, Score: {best_score}")
        return best_score, best_move


    def render_turn(self):
        font = pygame.font.Font(None, 36)
        turn_text = f"Turn: {PIECE_CHAR[self.engine.side]}"
        text_surface = font.render(turn_text, True, LINE_COLOR)
        self.screen.blit(text_surface, (10, SCREEN_HEIGHT - 40))

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)

            if self.engine.side == self.ai:
                _, best_move = self.handle_ai()
                row, col = best_move
                if self.engine.make_move(row, col):
                    if self.engine.is_winning(self.engine.get_reverse_side()):
                        print(f"{PIECE_CHAR[self.engine.get_reverse_side()]} wins!")
                        self.running = False
                else:
                    raise Exception("AI made illegal move")


            self.draw_board()
            self.draw_pieces()
            self.render_turn()
            pygame.display.flip()

        pygame.quit()


def negamax_with_alphabeta(engine, depth, alpha, beta, color):
    if  engine.is_winning(engine.get_reverse_side()):
        return color * 100000, None
    if depth == 0:
        return color * engine.evaluate(engine.side), None

    best_score = float('-inf')
    best_move = None

    for row in range(BOARD_ROW):
        for col in range(BOARD_COLUMN):
            if engine.board[row][col] == EMPTY: 
                
                engine.make_move(row, col)

                
                score, _ = negamax_with_alphabeta(engine, depth - 1, -beta, -alpha, -color)

                
                engine.undo_move()

                
                score = -score

                
                if score > best_score:
                    best_score = score
                    best_move = (row, col)

                
                alpha = max(alpha, score)
                if alpha >= beta:
                    break

    return best_score, best_move



if __name__ == "__main__":
    gui = GomokuGUI()
    gui.run()
