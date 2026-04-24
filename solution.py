
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

class ChessPiece:
  def __init__(self):
    self.valid_moves = []
  def is_move_valid(self,board, from_row, from_col, to_row, to_col):
    raise NotImplementedError("Subclasses must implement this method!")
  def get_valid_moves(self, board, from_row, from_col, color):
    raise NotImplementedError("Subclasses must implement this method!")


def normalize_white_directions(directions):
  for i in range(directions):
    directions[i] = -directions[i]

  return directions

def add_cells(cell1, cell2):
  return [cell1[0]+cell2[0], cell1[1]+cell2[1]]

class Pawn(ChessPiece):


  def is_move_valid(self,board, from_row, from_col, to_row, to_col):
    pass

  def get_valid_moves(self, board, from_row, from_col, color):
    directions = [[1,0], [2,0], [1,1], [1,-1]]
    if (color == COLORS.W):
      directions = normalize_white_directions(directions)


    for i in range(4):
      added_cell = add_cells(directions[i], [from_row, from_col])
      if (i==0 or i==1):
        if board[added_cell[0]][added_cell[1]] == None: self.valid_moves.push(added_cell)
      else:
        if board[added_cell[0]][added_cell[1]] != None: self.valid_moves.push(added_cell)

    return self.valid_moves;

    



class Rook(ChessPiece):
  def is_move_valid(self,board, from_row, from_col, to_row, to_col):
    pass

  def get_valid_moves(self, board, from_row, from_col, color):
    pass

class Knight(ChessPiece):
  def is_move_valid(self,board, from_row, from_col, to_row, to_col):
    pass

  def get_valid_moves(self, board, from_row, from_col, color):
    pass

class Bishop(ChessPiece):
  def is_move_valid(self,board, from_row, from_col, to_row, to_col):
    pass

  def get_valid_moves(self, board, from_row, from_col, color):
    pass

class Queen(ChessPiece):
  def is_move_valid(self,board, from_row, from_col, to_row, to_col):
    pass

  def get_valid_moves(self, board, from_row, from_col, color):
    pass

class King(ChessPiece):
  def is_move_valid(self,board, from_row, from_col, to_row, to_col):
    pass

  def get_valid_moves(self, board, from_row, from_col, color):
    pass

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


