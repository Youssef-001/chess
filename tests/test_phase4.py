import pytest
from solution import Chess


def make_piece(type, color):
    return {'type': type, 'color': color}


# ─── Helpers ────────────────────────────────────────────────────────────────

def fools_mate(chess, gameId):
    chess.movePiece(gameId, 6, 5, 5, 5)
    chess.movePiece(gameId, 1, 4, 3, 4)
    chess.movePiece(gameId, 6, 6, 4, 6)
    chess.movePiece(gameId, 0, 3, 4, 7)


# ─── createGame returns unique IDs ──────────────────────────────────────────

class TestCreateGame:
    def test_returns_a_game_id(self):
        chess = Chess()
        gameId = chess.createGame()
        assert gameId is not None

    def test_returns_unique_ids(self):
        chess = Chess()
        ids = {chess.createGame() for _ in range(10)}
        assert len(ids) == 10

    def test_game_id_is_string(self):
        chess = Chess()
        gameId = chess.createGame()
        assert isinstance(gameId, str)

    def test_each_game_starts_with_fresh_board(self):
        chess = Chess()
        g1 = chess.createGame()
        g2 = chess.createGame()
        assert chess.getGameState(g1)['board'] == chess.getGameState(g2)['board']


# ─── Isolation between games ─────────────────────────────────────────────────

class TestGameIsolation:
    def test_move_in_game1_does_not_affect_game2(self):
        chess = Chess()
        g1 = chess.createGame()
        g2 = chess.createGame()
        chess.movePiece(g1, 6, 4, 4, 4)
        board2 = chess.getGameState(g2)['board']
        assert board2[4][4] is None
        assert board2[6][4] == make_piece('P', 'white')

    def test_move_in_game2_does_not_affect_game1(self):
        chess = Chess()
        g1 = chess.createGame()
        g2 = chess.createGame()
        chess.movePiece(g2, 6, 3, 4, 3)
        board1 = chess.getGameState(g1)['board']
        assert board1[4][3] is None
        assert board1[6][3] == make_piece('P', 'white')

    def test_turn_order_is_independent_per_game(self):
        chess = Chess()
        g1 = chess.createGame()
        g2 = chess.createGame()

        chess.movePiece(g1, 6, 4, 4, 4)   # g1: white moves
        chess.movePiece(g1, 1, 4, 3, 4)   # g1: black moves
        # g2 has had no moves — still white's turn
        chess.movePiece(g2, 1, 4, 3, 4)   # g2: black tries first — should be ignored
        board2 = chess.getGameState(g2)['board']
        assert board2[3][4] is None
        assert board2[1][4] == make_piece('P', 'black')

    def test_status_independent_per_game(self):
        chess = Chess()
        g1 = chess.createGame()
        g2 = chess.createGame()
        fools_mate(chess, g1)
        assert chess.getGameState(g1)['status'] == 'black won'
        assert chess.getGameState(g2)['status'] == 'ongoing'

    def test_game_over_in_one_does_not_freeze_other(self):
        chess = Chess()
        g1 = chess.createGame()
        g2 = chess.createGame()
        fools_mate(chess, g1)
        chess.movePiece(g2, 6, 4, 4, 4)
        board2 = chess.getGameState(g2)['board']
        assert board2[4][4] == make_piece('P', 'white')

    def test_many_games_independent(self):
        chess = Chess()
        ids = [chess.createGame() for _ in range(5)]
        # Move pawn in each game to a different column
        for i, gid in enumerate(ids):
            chess.movePiece(gid, 6, i, 4, i)
        for i, gid in enumerate(ids):
            board = chess.getGameState(gid)['board']
            assert board[4][i] == make_piece('P', 'white')
            # Other games' columns should be untouched in this game
            for j in range(5):
                if j != i:
                    assert board[4][j] is None


# ─── getGameState per gameId ─────────────────────────────────────────────────

class TestGetGameState:
    def test_returns_board_key(self):
        chess = Chess()
        gid = chess.createGame()
        assert 'board' in chess.getGameState(gid)

    def test_returns_status_key(self):
        chess = Chess()
        gid = chess.createGame()
        assert 'status' in chess.getGameState(gid)

    def test_initial_status_ongoing(self):
        chess = Chess()
        gid = chess.createGame()
        assert chess.getGameState(gid)['status'] == 'ongoing'

    def test_board_reflects_moves(self):
        chess = Chess()
        gid = chess.createGame()
        chess.movePiece(gid, 6, 4, 4, 4)
        board = chess.getGameState(gid)['board']
        assert board[4][4] == make_piece('P', 'white')
        assert board[6][4] is None


# ─── movePiece per gameId ────────────────────────────────────────────────────

class TestMovePiece:
    def test_valid_move_updates_correct_game(self):
        chess = Chess()
        g1 = chess.createGame()
        g2 = chess.createGame()
        chess.movePiece(g1, 6, 0, 4, 0)
        assert chess.getGameState(g1)['board'][4][0] == make_piece('P', 'white')
        assert chess.getGameState(g2)['board'][4][0] is None

    def test_interleaved_moves_across_games(self):
        chess = Chess()
        g1 = chess.createGame()
        g2 = chess.createGame()
        chess.movePiece(g1, 6, 4, 4, 4)   # g1 white
        chess.movePiece(g2, 6, 3, 4, 3)   # g2 white
        chess.movePiece(g1, 1, 4, 3, 4)   # g1 black
        chess.movePiece(g2, 1, 3, 3, 3)   # g2 black
        assert chess.getGameState(g1)['board'][3][4] == make_piece('P', 'black')
        assert chess.getGameState(g2)['board'][3][3] == make_piece('P', 'black')

    def test_move_after_game_over_ignored(self):
        chess = Chess()
        gid = chess.createGame()
        fools_mate(chess, gid)
        board_before = chess.getGameState(gid)['board']
        chess.movePiece(gid, 6, 0, 5, 0)
        board_after = chess.getGameState(gid)['board']
        assert board_before == board_after
