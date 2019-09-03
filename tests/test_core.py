from unittest import TestCase
from unittest.mock import patch
from models.core import Player, MarkType, Deck, AbstractGame


class PlayerTestCase(TestCase):

    def test_raise_error_if_mark_is_invalid(self):
        player_1 = Player(MarkType.CROSS, 'playerName')
        with self.assertRaises(TypeError):
            player_2 = Player(MarkType.EMPTY, 'playerName')
        with self.assertRaises(TypeError):
            player_2 = Player('not a mark', 'playerName')

    def test_should_keep_mark(self):
        player_1 = Player(MarkType.CROSS, 'playerName')
        self.assertEqual(player_1.mark, MarkType.CROSS)

        player_2 = Player(MarkType.NOUGHT, 'playerName')
        self.assertEqual(player_2.mark, MarkType.NOUGHT)


class DeckTestCase(TestCase):

    def setUp(self) -> None:
        self.deck = Deck(3)

    def test_creates_square_matrix_of_provided_size(self):
        deck_3_3 = Deck(3)
        self.assertEqual(len(deck_3_3._deck), 3)
        for row in deck_3_3._deck:
            self.assertEqual(len(row), 3)

        deck_5_5 = Deck(5)
        self.assertEqual(len(deck_5_5._deck), 5)
        for row in deck_5_5._deck:
            self.assertEqual(len(row), 5)

    def test_creates_matrix_with_all_empty_cells(self):
        for row in self.deck._deck:
            for cell in row:
                self.assertEqual(cell, MarkType.EMPTY)

    def test_put_mark(self):
        self.deck.put_mark(1, 1, MarkType.NOUGHT)
        self.assertEqual(self.deck._deck[1][1], MarkType.NOUGHT)
        self.deck.put_mark(2, 2, MarkType.CROSS)
        self.assertEqual(self.deck._deck[2][2], MarkType.CROSS)

    def test_has_empty_cells(self):
        for x, row in enumerate(self.deck._deck):
            for y, cell in enumerate(row):
                self.deck._deck[x][y] = MarkType.CROSS
        self.assertFalse(self.deck.has_empty_cells())

        self.deck._deck[2][2] = MarkType.EMPTY
        self.assertTrue(self.deck.has_empty_cells())

    def test_get_row_return_row_copy(self):
        row = self.deck.get_row(0)
        for idx, cell in enumerate(row):
            self.assertEqual(self.deck._deck[0][idx], cell)

        self.assertEqual(row[0], self.deck._deck[0][0])
        row[0] = '42'
        self.assertNotEqual(row[0], self.deck._deck[0][0])

    def test_get_all_rows(self):
        all_rows = self.deck.get_all_rows()
        for x, row in enumerate(all_rows):
            for y, cell in enumerate(row):
                self.assertEqual(all_rows[x][y], self.deck._deck[x][y])


class AbstractGameTestCase(TestCase):

    def setUp(self) -> None:
        self.player_1 = Player(MarkType.CROSS, 'playerName')
        self.player_2 = Player(MarkType.NOUGHT, 'playerName')
        self.deck = Deck(3)
        self.game = AbstractGame([self.player_1, self.player_2], self.deck)

    def test_keep_players_and_deck(self):
        self.assertEqual(self.game._deck, self.deck)
        self.assertEqual(self.game._players, [self.player_1, self.player_2])

    @patch('models.core.Deck.put_mark')
    def test_put_mark(self, put_mark_mock):
        self.game._put_mark(1, 2)
        put_mark_mock.assert_called_once_with(1, 2, self.game.current_player.mark)

    def test_pass_turn_to_next_player(self):
        self.assertEqual(self.game._current_player_index, 0)
        self.assertEqual(self.game.current_player, self.player_1)
        self.game._pass_turn_to_next_player()
        self.assertEqual(self.game._current_player_index, 1)
        self.assertEqual(self.game.current_player, self.player_2)

    @patch('models.core.AbstractGame._check_for_winner')
    @patch('models.core.AbstractGame._put_mark')
    @patch('models.core.Deck.has_empty_cells')
    @patch('models.core.AbstractGame._pass_turn_to_next_player')
    def test_make_turn_without_ending(self, to_next_player, has_empty_cells, put_mark, check_for_winner):
        check_for_winner.return_value = False
        self.game.make_turn(0, 0)
        put_mark.assert_called_once_with(0, 0)
        has_empty_cells.assert_called_once()
        to_next_player.assert_called_once()

    @patch('models.core.AbstractGame._end_game_with_winner')
    @patch('models.core.AbstractGame._check_for_winner')
    @patch('models.core.AbstractGame._put_mark')
    @patch('models.core.Deck.has_empty_cells')
    @patch('models.core.AbstractGame._pass_turn_to_next_player')
    def test_make_turn_with_winner(self, to_next_player, has_empty_cells, put_mark, check_for_winner, mock_for_win):
        check_for_winner.return_value = True
        self.game.make_turn(0, 0)
        put_mark.assert_called_once_with(0, 0)
        has_empty_cells.assert_not_called()
        to_next_player.assert_not_called()
        mock_for_win.assert_called_once()

    @patch('models.core.AbstractGame._end_game_with_tie')
    @patch('models.core.AbstractGame._check_for_winner')
    @patch('models.core.AbstractGame._put_mark')
    @patch('models.core.Deck.has_empty_cells')
    @patch('models.core.AbstractGame._pass_turn_to_next_player')
    def test_make_turn_with_tie(self, to_next_player, has_empty_cells, put_mark, check_for_winner, mock_for_tie):
        check_for_winner.return_value = False
        has_empty_cells.return_value = False
        self.game.make_turn(0, 0)
        put_mark.assert_called_once_with(0, 0)
        has_empty_cells.assert_called()
        to_next_player.assert_not_called()
        mock_for_tie.assert_called_once()

