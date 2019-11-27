import random
from abc import abstractmethod

from black_jack_descriptor import immutable
from black_jack_collections import ImmutableList


class Card:
    _card_score = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

    def __init__(self, *, num=None, color=None):
        self.num = num
        self.color = color
        self.score = self._card_score[num] if num else 0

    def __add__(self, other):
        """
        目前仅作计分用
        :param other:
        :return:
        """
        c = Card()
        c.score = self.score + other.score
        return c


class ConsoleCard(Card):
    _card_colors = ImmutableList(['♠', '♥', '♣', '♦'])
    _card_num = ImmutableList(['A', '2', '3', '4', '5', '6', '7',
                               '8', '9', '10', 'J', 'Q', 'K'])

    def __str__(self):
        return f'''
         _______
        |       |
        |   {self._card_colors[self.color]}   |
        |   {self._card_num[self.num]}   |
        |_______|
        '''


class ConsoleCardBack(ConsoleCard):
    def __str__(self):
        return '''
         _______
        |       |
        |   ++  |
        |   ++  |
        |_______|
        '''


class Pile:

    def __init__(self):
        self._card_indexes = [x for x in range(52)]
        self._card_indexes_it = None
        self.cut_cards()

    @immutable
    def cards(self):
        return self._cards

    def cut_cards(self):
        random.shuffle(self._card_indexes)
        self._card_indexes_it = iter(self._card_indexes)

    def get_card(self):
        try:
            return self.cards[next(self._card_indexes_it)]
        except StopIteration:
            print('no card')


class ConsolePile(Pile):
    def __init__(self):
        self._cards = ImmutableList(ConsoleCard(num=num, color=color) for num in range(13) for color in range(4))
        super().__init__()