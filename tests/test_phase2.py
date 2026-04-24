import pytest
from solution import Chess


def make_piece(type, color):
    return {'type': type, 'color': color}


# ─── Pawn ────────────────────────────────────────────────────────────────────

class TestPawn:
    def test_white_pawn_one_square_forward(self):
        chess = Chess()
        chess.createGame()
        chess.movePiece(6, 4, 5, 4)
        board = chess.getGameState()['board']
        assert board[5][4] == make_piece('P', 'white')
        assert board[6][4] is None

    def test_white_pawn_two_squares_from_start(self):
        chess = Chess()
        chess.createGame()
        chess.movePiece(6, 4, 4, 4)
        board = chess.getGameState()['board']
        assert board[4][4] == make_piece('P', 'white')

    def test_black_pawn_one_square_forward(self):
        chess = Chess()
        chess.createGame()
        chess.movePiece(6, 0, 5, 0)   # white moves first
        chess.movePiece(1, 4, 2, 4)   # black one square
        board = chess.getGameState()['board']
        assert board[2][4] == make_piece('P', 'black')

    def test_black_pawn_two_squares_from_start(self):
        chess = Chess()
        chess.createGame()
        chess.movePiece(6, 0, 5, 0)
        chess.movePiece(1, 4, 3, 4)
        board = chess.getGameState()['board']
        assert board[3][4] == make_piece('P', 'black')

    def test_pawn_cannot_move_two_squares_after_first_move(self):
        chess = Chess()
        chess.createGame()
        chess.movePiece(6, 4, 5, 4)   # white one square
        chess.movePiece(1, 0, 2, 0)   # black filler
        chess.movePiece(5, 4, 3, 4)   # white tries two squares — not on starting row
        board = chess.getGameState()['board']
        assert board[5][4] == make_piece('P', 'white')  # still there
        assert board[3][4] is None

    def test_pawn_blocked_by_piece_in_front(self):
        chess = Chess()
        chess.createGame()
        chess.movePiece(6, 4, 4, 4)   # white pawn e4
        chess.movePiece(1, 4, 3, 4)   # black pawn e5 — now directly in front
        chess.movePiece(4, 4, 3, 4)   # white tries to move forward into black — blocked
        board = chess.getGameState()['board']
        assert board[4][4] == make_piece('P', 'white')  # white still at e4
        assert board[3][4] == make_piece('P', 'black')  # black still at e5

    def test_pawn_diagonal_capture(self):
        chess = Chess()
        chess.createGame()
        chess.movePiece(6, 4, 4, 4)   # white e4
        chess.movePiece(1, 3, 3, 3)   # black d5
        chess.movePiece(4, 4, 3, 3)   # white captures diagonally
        board = chess.getGameState()['board']
        assert board[3][3] == make_piece('P', 'white')

    def test_pawn_cannot_capture_forward(self):
        chess = Chess()
        chess.createGame()
        # Place pieces so there is an enemy in front
        chess.movePiece(6, 4, 4, 4)
        chess.movePiece(1, 4, 3, 4)
        chess.movePiece(4, 4, 3, 4)   # not a diagonal — should be blocked
        board = chess.getGameState()['board']
        assert board[4][4] == make_piece('P', 'white')

    def test_pawn_cannot_move_backward(self):
        chess = Chess()
        chess.createGame()
        chess.movePiece(6, 4, 5, 4)   # white
        chess.movePiece(1, 0, 2, 0)   # black filler
        chess.movePiece(5, 4, 6, 4)   # white tries to move back — illegal
        board = chess.getGameState()['board']
        assert board[5][4] == make_piece('P', 'white')


# ─── Knight ──────────────────────────────────────────────────────────────────

class TestKnight:
    def test_knight_valid_l_shape(self):
        chess = Chess()
        chess.createGame()
        chess.movePiece(7, 6, 5, 5)   # white Ng1 -> f3
        board = chess.getGameState()['board']
        assert board[5][5] == make_piece('N', 'white')
        assert board[7][6] is None

    def test_knight_can_jump_over_pieces(self):
        chess = Chess()
        chess.createGame()
        # b1 knight can jump out immediately without clearing pawns
        chess.movePiece(7, 1, 5, 2)   # Nb1 -> c3
        board = chess.getGameState()['board']
        assert board[5][2] == make_piece('N', 'white')

    def test_knight_invalid_move(self):
        chess = Chess()
        chess.createGame()
        chess.movePiece(7, 6, 5, 6)   # not an L-shape
        board = chess.getGameState()['board']
        assert board[7][6] == make_piece('N', 'white')

    def test_knight_cannot_land_on_friendly(self):
        chess = Chess()
        chess.createGame()
        # Ng1 to e2 would land on a white pawn — illegal
        chess.movePiece(7, 6, 6, 4)
        board = chess.getGameState()['board']
        assert board[7][6] == make_piece('N', 'white')


# ─── Rook ─────────────────────────────────────────────────────────────────────

class TestRook:
    def test_rook_valid_vertical_move(self):
        chess = Chess()
        chess.createGame()
        chess.movePiece(6, 0, 4, 0)   # clear pawn path
        chess.movePiece(1, 0, 2, 0)   # black filler
        chess.movePiece(7, 0, 5, 0)   # rook moves up
        board = chess.getGameState()['board']
        assert board[5][0] == make_piece('R', 'white')

    def test_rook_blocked_by_piece(self):
        chess = Chess()
        chess.createGame()
        chess.movePiece(7, 0, 5, 0)   # rook can't — pawn in the way
        board = chess.getGameState()['board']
        assert board[7][0] == make_piece('R', 'white')

    def test_rook_valid_horizontal_move(self):
        chess = Chess()
        chess.createGame()
        chess.movePiece(6, 0, 4, 0)   # white pawn
        chess.movePiece(1, 0, 2, 0)   # black filler
        chess.movePiece(7, 0, 6, 0)   # rook to row 6
        chess.movePiece(1, 1, 2, 1)   # black filler
        chess.movePiece(6, 0, 5, 0)   # rook moves horizontally along row 6
        # Actually move rook horizontally
        chess2 = Chess()
        chess2.createGame()
        chess2.movePiece(6, 0, 4, 0)
        chess2.movePiece(1, 0, 2, 0)
        chess2.movePiece(7, 0, 5, 0)
        chess2.movePiece(1, 1, 2, 1)
        chess2.movePiece(5, 0, 5, 4)   # horizontal move
        board = chess2.getGameState()['board']
        assert board[5][4] == make_piece('R', 'white')

    def test_rook_cannot_move_diagonally(self):
        chess = Chess()
        chess.createGame()
        chess.movePiece(6, 0, 4, 0)
        chess.movePiece(1, 0, 2, 0)
        chess.movePiece(7, 0, 5, 0)
        chess.movePiece(1, 1, 2, 1)
        chess.movePiece(5, 0, 4, 1)   # diagonal — illegal
        board = chess.getGameState()['board']
        assert board[5][0] == make_piece('R', 'white')


# ─── Bishop ───────────────────────────────────────────────────────────────────

class TestBishop:
    def test_bishop_valid_diagonal(self):
        chess = Chess()
        chess.createGame()
        chess.movePiece(6, 3, 4, 3)   # open diagonal for c1 bishop
        chess.movePiece(1, 0, 2, 0)
        chess.movePiece(7, 2, 4, 5)   # Bc1 -> f4
        board = chess.getGameState()['board']
        assert board[4][5] == make_piece('B', 'white')

    def test_bishop_blocked_diagonally(self):
        chess = Chess()
        chess.createGame()
        chess.movePiece(7, 2, 5, 4)   # blocked by pawn at (6,3)
        board = chess.getGameState()['board']
        assert board[7][2] == make_piece('B', 'white')

    def test_bishop_cannot_move_straight(self):
        chess = Chess()
        chess.createGame()
        chess.movePiece(6, 3, 4, 3)
        chess.movePiece(1, 0, 2, 0)
        chess.movePiece(7, 2, 5, 2)   # straight — illegal for bishop
        board = chess.getGameState()['board']
        assert board[7][2] == make_piece('B', 'white')


# ─── Queen ────────────────────────────────────────────────────────────────────

class TestQueen:
    def test_queen_moves_vertically(self):
        chess = Chess()
        chess.createGame()
        chess.movePiece(6, 3, 4, 3)
        chess.movePiece(1, 0, 2, 0)
        chess.movePiece(7, 3, 5, 3)   # Qd1 -> d3
        board = chess.getGameState()['board']
        assert board[5][3] == make_piece('Q', 'white')

    def test_queen_moves_diagonally(self):
        chess = Chess()
        chess.createGame()
        chess.movePiece(6, 4, 4, 4)
        chess.movePiece(1, 0, 2, 0)
        chess.movePiece(7, 3, 3, 7)   # Qd1 -> h5
        board = chess.getGameState()['board']
        assert board[3][7] == make_piece('Q', 'white')

    def test_queen_blocked_by_piece(self):
        chess = Chess()
        chess.createGame()
        chess.movePiece(7, 3, 5, 3)   # queen blocked by own pawn
        board = chess.getGameState()['board']
        assert board[7][3] == make_piece('Q', 'white')


# ─── King ─────────────────────────────────────────────────────────────────────

class TestKing:
    def test_king_moves_one_square(self):
        chess = Chess()
        chess.createGame()
        chess.movePiece(6, 4, 5, 4)   # clear e-pawn
        chess.movePiece(1, 0, 2, 0)
        chess.movePiece(7, 4, 6, 4)   # king moves forward
        board = chess.getGameState()['board']
        assert board[6][4] == make_piece('K', 'white')

    def test_king_cannot_move_two_squares(self):
        chess = Chess()
        chess.createGame()
        chess.movePiece(6, 4, 5, 4)
        chess.movePiece(1, 0, 2, 0)
        chess.movePiece(7, 4, 5, 4)   # two squares — illegal
        board = chess.getGameState()['board']
        assert board[7][4] == make_piece('K', 'white')

    def test_king_cannot_capture_friendly(self):
        chess = Chess()
        chess.createGame()
        chess.movePiece(7, 4, 6, 4)   # king tries to move onto own pawn — illegal
        board = chess.getGameState()['board']
        assert board[7][4] == make_piece('K', 'white')


# ─── Friendly fire ───────────────────────────────────────────────────────────

class TestFriendlyFire:
    def test_cannot_capture_own_piece(self):
        chess = Chess()
        chess.createGame()
        chess.movePiece(7, 0, 6, 0)   # rook tries to land on own pawn
        board = chess.getGameState()['board']
        assert board[7][0] == make_piece('R', 'white')
        assert board[6][0] == make_piece('P', 'white')
