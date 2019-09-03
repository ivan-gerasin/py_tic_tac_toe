from enum import Enum, unique
from typing import Optional


@unique
class MarkType(Enum):
    EMPTY = ''
    NOUGHT = 'O'
    CROSS = 'X'


class Player:
    _name: str
    _mark: MarkType
    valid_player_marks = (MarkType.NOUGHT, MarkType.CROSS)

    def __init__(self, mark: MarkType, name):
        if mark not in self.valid_player_marks:
            raise TypeError(f'{mark} is incorrect player mark type')
        self._mark = mark
        self._name = name

    @property
    def mark(self):
        return self._mark

    def name(self):
        return self._name

class Deck:
    _deck: [[MarkType]]

    def __init__(self, size: int):
        self._deck = [[MarkType.EMPTY for x in range(size)] for y in range(size)]

    def put_mark(self, row: int, col: int, mark: MarkType):
        self._deck[row][col] = mark

    def has_empty_cells(self) -> bool:
        for row in self._deck:
            has_empty_cell = [True for col in row if col == MarkType.EMPTY]
            if has_empty_cell:
                return True
        return False

    def get_row(self, row: int) -> [MarkType]:
        return self._deck[row][:]

    def get_col(self, col_index: int) -> [MarkType]:
        col = []
        for row in self._deck:
            col.append(row[col_index])
        return col

    def get_all_rows(self):
        return [self.get_row(idx) for idx in range(len(self._deck))]

    def get_all_cols(self):
        return [self.get_col(idx) for idx in range(len(self._deck))]

    def get_main_diagonal(self):
        return [self._deck[idx][idx] for idx in range(len(self._deck))]

    def get_secondary_diagonal(self):
        row_len = len(self._deck)
        return [self._deck[row_len-idx][idx] for idx in range(row_len)]


class AbstractGame:
    _current_player_index: int = 0
    _players: [Player]
    _deck: Deck

    def __init__(self, players: [Player], deck: Deck):
        self._players = players[:]
        self._deck = deck
        marks = set([player.mark for player in players])
        if marks != len(players):
            raise TypeError('Some players have same mark')

    def make_turn(self, row: int, col: int):
        self._put_mark(row, col)
        if not self._deck.has_empty_cells():
            winner = self._check_for_winner()
            if winner:
                return self._end_game_with_winner(winner)
            return self._end_game_with_tie()
        self._pass_turn_to_next_player()

    def _put_mark(self, row: int, col: int):
        self._deck.put_mark(row, col, self._get_current_player_mark())

    def _get_current_player_mark(self) -> MarkType:
        return self._players[self._current_player_index].mark

    def _check_for_winner(self) -> Optional[Player]:
        raise NotImplementedError('Win condition is not defined')

    def _end_game_with_winner(self, winner: Player):
        raise NotImplementedError('Game ending is not defined')

    def _end_game_with_tie(self):
        raise NotImplementedError('Game ending is not defined')

    def _pass_turn_to_next_player(self):
        if self._current_player_index >= len(self._players)-1:
            self._current_player_index = 0
        else:
            self._current_player_index += 1

    def get_player_by_mark(self, mark: MarkType):
        return next(player for player in self._players if player.mark is mark)

    @property
    def current_player(self):
        return self._players[self._current_player_index]


class ClassicGame(AbstractGame):

    def _check_for_winner(self) -> Optional[Player]:
        directions = [
            self._deck.get_all_rows,
            self._deck.get_all_cols,
            self._deck.get_main_diagonal,
            self._deck.get_secondary_diagonal
        ]
        for seq_extractor in directions:
            winner = self._check_list_of_seq_for_winner(seq_extractor())
            if winner:
                return winner

    def _check_list_of_seq_for_winner(self, seqs: [[MarkType]]) -> Optional[Player]:
        for single_seq in seqs:
            if self._check_sequence(single_seq):
                return self.get_player_by_mark(single_seq[0])

    @staticmethod
    def _check_sequence(seq: [MarkType]) -> bool:
        all_same = len(set(seq)) == 1
        return all_same and seq[0] != MarkType.EMPTY

    def _end_game_with_winner(self, winner: Player):
        print(f'And winner is ${winner.name}')

    def _end_game_with_tie(self):
        print('No winner')




