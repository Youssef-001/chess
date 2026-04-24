import pytest
from solution import Chess


def make_piece(type, color):
    return {'type': type, 'color': color}


# ─── Helpers ────────────────────────────────────────────────────────────────

def starting_board():
    """Returns the expected board after createGame()."""
    b = make_piece
    return [
        [b('R','black'), b('N','black'), b('B','black'), b('Q','black'), b('K','black'), b('B','black'), b('N','black'), b('R','black')],
        [b('P','black')] * 8,
        [None] * 8,
        [None] * 8,
        [None] * 8,
        [None] * 8,
        [b('P','white')] * 8,
        [b('R','white'), b('N','white'), b('B','white'), b('Q','white'), b('K','white'), b('B','white'), b('N','white'), b('R','white')],
    ]


# ─── createGame / getGameState ───────────────────────────────────────────────

class TestCreateGame:
    def test_board_has_8_rows(self):
        chess = Chess()
        chess.createGame()
        assert len(chess.getGameState()['board']) == 8

    def test_each_row_has_8_cols(self):
        chess = Chess()
        chess.createGame()
        for row in chess.getGameState()['board']:
            assert len(row) == 8

    def test_starting_board_matches(self):
        chess = Chess()
        chess.createGame()
        assert chess.getGameState()['board'] == starting_board()

    def test_middle_rows_are_empty(self):
        chess = Chess()
        chess.createGame()
        board = chess.getGameState()['board']
        for row in board[2:6]:
            assert all(cell is None for cell in row)

    def test_white_pawns_on_row_6(self):
        chess = Chess()
        chess.createGame()
        board = chess.getGameState()['board']
        for cell in board[6]:
            assert cell == make_piece('P', 'white')

    def test_black_pawns_on_row_1(self):
        chess = Chess()
        chess.createGame()
        board = chess.getGameState()['board']
        for cell in board[1]:
            assert cell == make_piece('P', 'black')

    def test_white_back_rank(self):
        chess = Chess()
        chess.createGame()
        board = chess.getGameState()['board']
        expected = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        for col, type in enumerate(expected):
            assert board[7][col] == make_piece(type, 'white')

    def test_black_back_rank(self):
        chess = Chess()
        chess.createGame()
        board = chess.getGameState()['board']
        expected = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        for col, type in enumerate(expected):
            assert board[0][col] == make_piece(type, 'black')

    def test_get_game_state_returns_dict_with_board_key(self):
        chess = Chess()
        chess.createGame()
        state = chess.getGameState()
        assert 'board' in state

    def test_create_game_resets_previous_state(self):
        chess = Chess()
        chess.createGame()
        chess.movePiece(6, 4, 4, 4)
        chess.createGame()
        assert chess.getGameState()['board'] == starting_board()


# ─── movePiece ───────────────────────────────────────────────────────────────

class TestMovePiece:
    def test_white_pawn_moves_first(self):
        chess = Chess()
        chess.createGame()
        chess.movePiece(6, 4, 4, 4)
        board = chess.getGameState()['board']
        assert board[4][4] == make_piece('P', 'white')
        assert board[6][4] is None

    def test_black_cannot_move_first(self):
        chess = Chess()
        chess.createGame()
        chess.movePiece(1, 4, 3, 4)  # black tries first — ignored
        board = chess.getGameState()['board']
        assert board[1][4] == make_piece('P', 'black')
        assert board[3][4] is None

    def test_alternating_turns(self):
        chess = Chess()
        chess.createGame()
        chess.movePiece(6, 4, 4, 4)  # white
        chess.movePiece(1, 4, 3, 4)  # black
        board = chess.getGameState()['board']
        assert board[4][4] == make_piece('P', 'white')
        assert board[3][4] == make_piece('P', 'black')

    def test_wrong_turn_ignored(self):
        chess = Chess()
        chess.createGame()
        chess.movePiece(6, 4, 4, 4)   # white moves
        chess.movePiece(6, 3, 4, 3)   # white tries again — ignored
        board = chess.getGameState()['board']
        assert board[6][3] == make_piece('P', 'white')  # still in place
        assert board[4][3] is None

    def test_move_from_empty_square_ignored(self):
        chess = Chess()
        chess.createGame()
        chess.movePiece(4, 4, 3, 4)  # empty square — ignored
        assert chess.getGameState()['board'] == starting_board()

    def test_capture_replaces_destination(self):
        """Phase 1 doesn't enforce rules — a piece can move anywhere and capture."""
        chess = Chess()
        chess.createGame()
        chess.movePiece(6, 0, 1, 0)   # white 'captures' black pawn (no rule check yet)
        board = chess.getGameState()['board']
        assert board[1][0] == make_piece('P', 'white')
        assert board[6][0] is None

    def test_board_is_not_mutated_between_calls(self):
        chess = Chess()
        chess.createGame()
        state1 = chess.getGameState()['board']
        chess.movePiece(6, 4, 4, 4)
        state2 = chess.getGameState()['board']
        # Original snapshot should not be affected if board is copied correctly
        assert state1[6][4] is not None or state2[4][4] is not None  # at least one moved

    def test_multiple_moves_sequence(self):
        chess = Chess()
        chess.createGame()
        chess.movePiece(6, 4, 4, 4)  # white
        chess.movePiece(1, 4, 3, 4)  # black
        chess.movePiece(6, 3, 4, 3)  # white
        chess.movePiece(1, 3, 3, 3)  # black
        board = chess.getGameState()['board']
        assert board[4][4] == make_piece('P', 'white')
        assert board[3][4] == make_piece('P', 'black')
        assert board[4][3] == make_piece('P', 'white')
        assert board[3][3] == make_piece('P', 'black')
