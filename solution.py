
from types import SimpleNamespace

PIECE_TYPES = SimpleNamespace(
K="K",
Q="Q",
N="N",
R="R",
B="B",
P="P"
)

COLORS = SimpleNamespace(
W="white",
B="black"
)

WHITE_FIRST_ROW = 7
WHITE_SECOND_ROW = 6
BLACK_FIRST_ROW = 0
BLACK_SECOND_ROW = 1

first_row_pieces = [PIECE_TYPES.R, PIECE_TYPES.N, PIECE_TYPES.B, PIECE_TYPES.Q, PIECE_TYPES.K, PIECE_TYPES.B, PIECE_TYPES.N, PIECE_TYPES.R]

  
def initialize_side(board, color, first_row_index, second_row_index):
  
  second_row = [{'type': PIECE_TYPES.P, 'color': color} for _ in range(8)]
  first_row = []
  for i in range(8):
    first_row.append({'type': first_row_pieces[i], 'color': color})

  board[first_row_index] = first_row
  board[second_row_index] = second_row




class Chess:
 def __init__(self):
    self.board = []
    self.player = COLORS.W

 def createGame(self):
   self.player = COLORS.W
   self.board = [[None  for _ in range(8)] for _ in range(8)]
   initialize_side(self.board, COLORS.W, WHITE_FIRST_ROW, WHITE_SECOND_ROW)
   initialize_side(self.board, COLORS.B, BLACK_FIRST_ROW, BLACK_SECOND_ROW)

 def next_player(self):
   self.player = COLORS.W if self.player == COLORS.B else COLORS.B

 def movePiece(self, from_row, from_col, to_row, to_col):
   if (self.board[from_row][from_col] == None): return
   if ((self.board[from_row][from_col])["color"] != self.player) : return

   self.board[to_row][to_col] = self.board[from_row][from_col]
   self.board[from_row][from_col] = None
   self.next_player();

 def getGameState(self):
   return {"board": self.board}


#   initialize_black()