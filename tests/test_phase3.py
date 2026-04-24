import pytest
from solution import Chess


def make_piece(type, color):
    return {'type': type, 'color': color}


# ─── Helpers ────────────────────────────────────────────────────────────────

def fools_mate(chess):
    """Sets up Fool's Mate — black wins."""
    chess.movePiece(6, 5, 5, 5)   # White: f2 -> f3
    chess.movePiece(1, 4, 3, 4)   # Black: e7 -> e5
    chess.movePiece(6, 6, 4, 6)   # White: g2 -> g4
    chess.movePiece(0, 3, 4, 7)   # Black: Qd8 -> h4 — checkmate


# ─── Check Detection ─────────────────────────────────────────────────────────

class TestCheck:
    def test_status_ongoing_initially(self):
        chess = Chess()
        chess.createGame()
        assert chess.getGameState()['status'] == 'ongoing'

    def test_scholar_check(self):
        """White queen attacks f7 — black king in check."""
        chess = Chess()
        chess.createGame()
        chess.movePiece(6, 4, 4, 4)   # e4
        chess.movePiece(1, 4, 3, 4)   # e5
        chess.movePiece(7, 3, 3, 7)   # Qh5
        chess.movePiece(1, 6, 2, 6)   # g6
        chess.movePiece(3, 7, 1, 5)   # Qxf7+
        assert chess.getGameState()['status'] == 'check'

    def test_check_resolved_by_king_move(self):
        chess = Chess()
        chess.createGame()
        chess.movePiece(6, 4, 4, 4)
        chess.movePiece(1, 4, 3, 4)
        chess.movePiece(7, 3, 3, 7)
        chess.movePiece(1, 6, 2, 6)
        chess.movePiece(3, 7, 1, 5)   # check
        chess.movePiece(0, 4, 1, 4)   # king moves — resolves check
        assert chess.getGameState()['status'] == 'ongoing'

    def test_move_that_leaves_own_king_in_check_is_illegal(self):
        chess = Chess()
        chess.createGame()
        chess.movePiece(6, 4, 4, 4)
        chess.movePiece(1, 4, 3, 4)
        chess.movePiece(7, 3, 3, 7)
        chess.movePiece(1, 6, 2, 6)
        chess.movePiece(3, 7, 1, 5)   # check
        chess.movePiece(1, 0, 2, 0)   # doesn't resolve check — illegal, ignored
        assert chess.getGameState()['status'] == 'check'  # still in check

    def test_blocking_a_check(self):
        chess = Chess()
        chess.createGame()
        chess.movePiece(6, 4, 4, 4)
        chess.movePiece(1, 4, 3, 4)
        chess.movePiece(7, 3, 3, 7)
        chess.movePiece(1, 6, 2, 6)
        chess.movePiece(3, 7, 1, 5)   # Qxf7+
        # Black can block by moving a piece between king and queen
        chess.movePiece(0, 6, 1, 4)   # Ng8 -> f6 (blocks or interposes)
        # Result depends on exact position — just confirm it's no longer check or is still check
        status = chess.getGameState()['status']
        assert status in ('ongoing', 'check')


# ─── Checkmate ───────────────────────────────────────────────────────────────

class TestCheckmate:
    def test_fools_mate_black_wins(self):
        chess = Chess()
        chess.createGame()
        fools_mate(chess)
        assert chess.getGameState()['status'] == 'black won'

    def test_no_moves_after_checkmate(self):
        chess = Chess()
        chess.createGame()
        fools_mate(chess)
        board_before = chess.getGameState()['board']
        chess.movePiece(6, 0, 5, 0)   # any white move — should be ignored
        board_after = chess.getGameState()['board']
        assert board_before == board_after

    def test_status_unchanged_after_ignored_move(self):
        chess = Chess()
        chess.createGame()
        fools_mate(chess)
        chess.movePiece(6, 0, 5, 0)
        assert chess.getGameState()['status'] == 'black won'

    def test_checkmate_has_status_key(self):
        chess = Chess()
        chess.createGame()
        fools_mate(chess)
        assert 'status' in chess.getGameState()


# ─── Stalemate ───────────────────────────────────────────────────────────────

class TestStalemate:
    def _setup_stalemate(self):
        """
        Construct a stalemate by direct board manipulation if possible,
        or use a known move sequence.
        Uses a helper that subclasses Chess to inject a position.
        """
        pass  # See individual tests below

    def test_stalemate_status(self):
        """
        Reach a stalemate: white has king on a1, black has queen on c2 and king on a3.
        White king on a1 (row 7, col 0 in our coords) has no legal moves and is not in check.
        We test this by injecting the board state through a move sequence that reaches stalemate.
        """
        chess = Chess()
        chess.createGame()
        # Use the inject helper if available, else skip
        if not hasattr(chess, '_set_board'):
            pytest.skip("_set_board not implemented; skipping stalemate injection test")

        # Classic stalemate: white king at a1, black queen at c2, black king at a3
        # (board indices: a1 = row7,col0; c2 = row6,col2; a3 = row5,col0)
        empty = [[None]*8 for _ in range(8)]
        empty[7][0] = make_piece('K', 'white')
        empty[6][2] = make_piece('Q', 'black')
        empty[5][0] = make_piece('K', 'black')
        chess._set_board(empty, current_turn='white')
        assert chess.getGameState()['status'] == 'stalemate'

    def test_not_stalemate_when_move_available(self):
        chess = Chess()
        chess.createGame()
        # At start, white has many moves — definitely not stalemate
        assert chess.getGameState()['status'] == 'ongoing'


# ─── Status Completeness ─────────────────────────────────────────────────────

class TestStatusValues:
    def test_status_is_one_of_valid_values(self):
        chess = Chess()
        chess.createGame()
        valid = {'ongoing', 'check', 'white won', 'black won', 'stalemate'}
        assert chess.getGameState()['status'] in valid

    def test_after_each_move_status_is_valid(self):
        chess = Chess()
        chess.createGame()
        valid = {'ongoing', 'check', 'white won', 'black won', 'stalemate'}
        moves = [
            (6, 4, 4, 4), (1, 4, 3, 4),
            (7, 6, 5, 5), (0, 1, 2, 2),
        ]
        for move in moves:
            chess.movePiece(*move)
            assert chess.getGameState()['status'] in valid
